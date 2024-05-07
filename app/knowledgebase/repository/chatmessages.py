from .. import schemas, models
from sqlalchemy.ext.asyncio import AsyncSession

async def create(request: schemas.CreateChatMessage, db: AsyncSession):
    message = models.ChatMessages(id = request.id, chatId = request.chatId,
                            question = request.question, answer = request.answer,
                            sources = request.sources)
    db.add(message)
    await db.flush()
    await db.refresh(message)
    return message
