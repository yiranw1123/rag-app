from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database
from fastapi import status, APIRouter, HTTPException
from ..repository import chatmessage
import json
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/chatmessages", tags=['chatmessages'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ChatMessage)
async def create(request: schemas.CreateChatMessage):
    async with database.get_db_context() as db:
        async with db.begin():
            try:
                message = await chatmessage.create(request, db)
                return schemas.ChatMessage(id = message.id, chatId = message.chatId,
                                        question = message.question, answer = message.answer,
                                        sources = json.dumps(message.sources), tagsList = [schemas.Tag(id = t.id, text = t.text) for t in message.tags])
            except SQLAlchemyError as e:
                print(e)
                raise HTTPException(status_code=500, detail="Database error.")