from .. import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

async def get_all(db: AsyncSession):
    stmt = select(models.Chat).order_by(desc(models.Chat.created))
    results= await db.execute(stmt)
    kbs = results.scalars().all()
    return kbs

async def create(request: schemas.CreateChat, db: AsyncSession):
    chat = models.Chat(chat_name = request.chat_name, kb_id = request.kb_id)
    db.add(chat)
    await db.flush()
    await db.refresh(chat)
    return chat.id