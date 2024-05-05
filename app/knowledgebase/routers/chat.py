from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from .. import database, schemas
from ..dependencies import get_chroma_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain
from typing import List
from ..repository import chat
from ..routers import knowledgebase
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ..store.utils.RedisStoreUtils import get_chat_history
from .utils.chatUtils import format_chat_history
import json
import cachetools

router = APIRouter(prefix="/chat", tags = ['chat'])
cache = cachetools.LRUCache(maxsize=1000)

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/', response_model=List[schemas.ShowChat])
async def all(db: AsyncSession= Depends(get_db)):
    data = await chat.get_all(db)
    return [schemas.ShowChat(chat_name=chat.chat_name, id = chat.id, kb_id=chat.kb_id) for chat in data]

@router.get('/kb_id/{kb_id}', response_model=schemas.ShowChat)
async def get_by_kbid(kb_id:int, db: AsyncSession= Depends(get_db)):
    c = await chat.get_by_kbid(kb_id, db)
    if not c:
        kb_details = await knowledgebase.get_by_id(kb_id, db)
        kb_name = kb_details.name

        # chat id will be the key to redis msg store
        c = await chat.create(schemas.CreateChat(chat_name = kb_name, kb_id=kb_id), db)
    return schemas.ShowChat(chat_name=c.chat_name, kb_id= c.kb_id, id = c.id)

@router.get('/{id}', response_model=schemas.ShowChat)
async def get_by_id(id: uuid.UUID, db: AsyncSession= Depends(get_db)):
    c = await chat.get_by_id(id, db)
    return schemas.ShowChat(chat_name=c.chat_name, id = c.id, kb_id=c.kb_id)

async def get_resp_from_retriever(id, retriever, msg):
    if msg in cache:
        print("found similar answer in cache")
    else:
        res = await retriever.ainvoke(
            {"input": msg},
            config={
                "configurable": {"session_id":id}
            })
        response = {"answer": res['answer'], "context": [doc.json() for doc in res['context']]}
        cache[msg] = response
    return json.dumps(cache[msg])

@router.get('/history/{chat_id}')
async def fetch_chat_history(chat_id = str):
    history = await get_chat_history(chat_id)
    formatted_history = await format_chat_history(history)
    return formatted_history

# id is the uuid for chat session with kb_id
async def post(websocket: WebSocket, id: str, db: AsyncSession= Depends(get_db)):
    await websocket.accept()

    details = await chat.get_by_id(uuid.UUID(id), db)
    kb_id = details.kb_id
    retriever = await get_retriever(kb_id, websocket.app.state.chroma)
    try:
        while True:
            data = await websocket.receive_text()
            response = await get_resp_from_retriever(id, retriever, data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for client {id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close(code=1000)
            print(f"Client {id} disconnected")

async def get_retriever(kb_id: int, chroma_client = Depends(get_chroma)):
    #check if a session with this kb_id already exists, if so load the history
    collection_name = f"{COLLECTION_PREFIX}{kb_id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)
    return chain
    
