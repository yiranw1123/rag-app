from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database,models
from fastapi import status, APIRouter, HTTPException
from ..repository import chatmessage
import json
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select


router = APIRouter(prefix="/chatmessages", tags=['chatmessages'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ChatMessage)
async def create(request: schemas.CreateChatMessage):
    async with database.get_db_context() as db:
        async with db.begin():
            try:
                message = await chatmessage.create(request, db)
                return schemas.ChatMessage(id = message.id, chat_id = message.chat_id,
                                        question = message.question, answer = message.answer,
                                        timestamp=message.timestamp, sources = json.dumps(message.sources),
                                        tags_list = [schemas.Tag(id = t.id, text = t.text) for t in message.tags])
            except HTTPException as http_exc:
                raise http_exc
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred{str(e)}")