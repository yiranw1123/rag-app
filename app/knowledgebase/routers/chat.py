from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from .. import database, schemas
from ..dependencies import get_chroma_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain
from ..repository import chat
from sqlalchemy.ext.asyncio import AsyncSession
from ..api.llm import process_and_get_answer
from typing import List
import uuid
import json
from cachetools import LRUCache, cached

router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/', response_model=List[schemas.ShowChat])
async def all(db: AsyncSession= Depends(get_db)):
    data = await chat.get_all(db)
    return [schemas.ShowChat(id = chat.id) for chat in data]

@router.get('/kb_id/{kb_id}', response_model=schemas.ShowChat)
async def get_by_kbid(kb_id:int, db: AsyncSession= Depends(get_db)):
    c = await chat.get_by_kbid(kb_id, db)
    if not c:
        # chat id will be the key to redis msg store
        c = await chat.create(schemas.CreateChat(kb_id=kb_id), db)
    return schemas.ShowChat(id = c.id)

@router.get('/{id}', response_model=schemas.ShowChat)
async def get_by_id(id: uuid.UUID, db: AsyncSession= Depends(get_db)):
    c = await chat.get_by_id(id, db)
    return schemas.ShowChat(id = c.id)

@cached(cache = LRUCache(maxsize=32))
@router.get('/history/{chat_id}')
async def fetch_chat_history(chat_id = str, db: AsyncSession= Depends(get_db)):
    history = await chat.fetch_history_by_id(chat_id, db)
    return history

# id is the uuid for chat session with kb_id
async def post(websocket: WebSocket, id: str, db: AsyncSession= Depends(get_db)):
    await websocket.accept()

    details = await chat.get_by_id(uuid.UUID(id), db)
    kb_id = details.kb_id
    retriever = await get_retriever(kb_id, websocket.app.state.chroma)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"received: {data}")
            # schemas.ChatMessage
            message_model = await process_and_get_answer(kb_id, id, data, retriever, db)
            response = {
                'answer': message_model.answer,
                'sources': message_model.sources,
                'tags': [t.model_dump_json() for t in message_model.tagsList]
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for client {id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close(code=1000)
            print(f"Client {id} disconnected")

async def get_retriever(kb_id: int, chroma_client = Depends(get_chroma)):
    collection_name = f"{COLLECTION_PREFIX}{kb_id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)
    return chain
    
