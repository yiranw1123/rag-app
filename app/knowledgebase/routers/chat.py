from fastapi import APIRouter, Depends, WebSocket
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
import json


router = APIRouter(prefix="/chat", tags = ['chat'])

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
    res = await retriever.ainvoke(
        {"input": msg},
        config={
            "configurable": {"session_id":id}
    })
    answer = res['answer']
    return answer

@router.get('/history/{chat_id}')
async def fetch_chat_history(chat_id = str):
    history = await get_chat_history(chat_id)
    
    formatted_messages = []
    for message_str in history:
        # Assuming each message is a JSON string; parse it
        message = json.loads(message_str)
        
        # Determine the sender based on the type of the message
        sender = "assistant" if message.get("type") == "ai" else "me"
        
        # Extract the content of the message
        content = message.get("data", {}).get("content", "")
        
        # Append formatted message to the list
        formatted_messages.append({"sender": sender, "text": content})

    return formatted_messages

# id is the uuid for chat session with kb_id
async def post(websocket: WebSocket, id: str, db: AsyncSession= Depends(get_db)):
    await websocket.accept()

    details = await chat.get_by_id(uuid.UUID(id), db)
    kb_id = details.kb_id
    retriever = await get_retriever(kb_id, websocket.app.state.chroma)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"echo: {data}")
            answer = await get_resp_from_retriever(id, retriever, data)
            await websocket.send_text(answer)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if not websocket.client_state == "DISCONNECTED":
            await websocket.close(code=1000)
            print(f"Client {id} disconnected")

async def get_retriever(kb_id: int, chroma_client = Depends(get_chroma)):
    #check if a session with this kb_id already exists, if so load the history
    collection_name = f"{COLLECTION_PREFIX}{kb_id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)
    return chain
    
