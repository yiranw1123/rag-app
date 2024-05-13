from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database
from fastapi import status, Depends, APIRouter
from ..repository import chatmessage
import json

get_db = database.get_db

router = APIRouter(prefix="/chatmessages", tags=['chatmessages'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ChatMessage)
async def create(request: schemas.CreateChatMessage, db: AsyncSession = Depends(get_db)):
    message = await chatmessage.create(request, db)
    return schemas.ChatMessage(id = message.id, chatId = message.chatId,
                               question = message.question, answer = message.answer,
                               sources = json.dumps(message.sources), tagsList = [schemas.Tag(id = t.id, text = t.text) for t in message.tags])