from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.exc import SQLAlchemyError
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
import uuid

router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/', response_model=List[schemas.ShowChat])
async def all(db: AsyncSession= Depends(get_db)):
    data = await chat.get_all(db)
    return [schemas.ShowChat(id = chat.id) for chat in data]

@router.get('/kb_id/{kb_id}', response_model=schemas.ShowChat)
async def get_by_kbid(kb_id:int, db: AsyncSession= Depends(get_db)):
    async with db.begin():
        try:
            c = await chat.get_by_kbid(kb_id, db)
            if not c:
                # chat id will be the key to redis msg store
                c = await chat.create(schemas.CreateChat(kb_id=kb_id), db)
            return schemas.ShowChat(id = c.id)
        except SQLAlchemyError as e:
            print("SQLAlchemy error occurred: %s", e)
            raise HTTPException(status_code=500, detail="Database error occurred.")
        except Exception as e:
            print("error occurred: %s", e)
            raise HTTPException(status_code=500, detail=e)

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
async def post(websocket: WebSocket, id: str):
    await websocket.accept()
    async with database.get_db_context() as db:
        details = await chat.get_by_id(uuid.UUID(id), db)
        kb_id = details.kb_id
        retriever = await get_retriever(kb_id, websocket.app.state.chroma)
        try:
            while True:
                data = await websocket.receive_text()
                receivedMsg = json.loads(data)
                print(f"received question: {receivedMsg['question']}")
                #schemas.ChatMessage
                message_model = await process_and_get_answer(kb_id, id, receivedMsg, retriever)
                #message_model = schemas.ChatMessage(id=uuid.UUID('ae487f3c-e013-4399-b6d7-647b65f446ea'), chat_id=uuid.UUID('44230cc4-1efc-4656-9d88-ad4933f89096'), question="what's taylor's occupation?", answer="Taylor Swift's occupation is a singer-songwriter. She has also directed music videos and films.", sources='{"documents": [{"doc_id": "5028f8dd-46d1-4d0b-827e-d42f24a4db8c", "page_content": "Taylor Swift is an American singer-songwriter who has had a significant impact on the music industry, popular culture, and politics. She began her career at the age of 14 and signed with Big Machine Records in 2005. Her albums have explored different styles such as country pop, rock, electronic, and indie folk, and she has released several number-one songs. Swift has also directed music videos and films, and her Eras Tour became the highest-grossing tour of all time."}, {"doc_id": "143465b6-3078-4580-be31-2c04a268c44c", "page_content": "Taylor Swift is a world-renowned singer-songwriter with numerous accolades and records to her name. She has sold over 200 million records and has been named Global Recording Artist of the Year three times. She is the highest-grossing female touring act, the most-streamed woman on Spotify and Apple Music, and the first billionaire with music as the main source of income. Swift has won numerous awards, including 14 Grammy Awards, a Primetime Emmy Award, 40 American Music Awards, 40 Billboard Music Awards, and 23 MTV Video Music Awards. She was born in Pennsylvania in 1989 and her parents were both involved in the financial industry. Her maternal grandmother was an opera singer."}, {"doc_id": "3793573d-d53f-482c-87cd-89ef640eff85", "page_content": "Taylor Swift is a world-renowned singer-songwriter with numerous accolades and records to her name. She has sold over 200 million records and has been named Global Recording Artist of the Year three times. She is the highest-grossing female touring act, the most-streamed woman on Spotify and Apple Music, and the first billionaire with music as the main source of income. Swift has won numerous awards, including 14 Grammy Awards, a Primetime Emmy Award, 40 American Music Awards, 40 Billboard Music Awards, and 23 MTV Video Music Awards. She was born in Pennsylvania in 1989 and her parents were both involved in the financial industry. Her maternal grandmother was an opera singer."}]}', tags_list='[{"id": 1, "text": "Taylor Swift", "embedding": null}, {"id": 2, "text": "singer-songwriter", "embedding": null}]', timestamp='1716680489586')
                response = message_model.model_dump_json()
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
    collection_name = f"{COLLECTION_PREFIX}{kb_id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)
    return chain
    
