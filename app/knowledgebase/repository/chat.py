from .. import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import uuid

async def get_all(db: AsyncSession):
    stmt = select(models.Chat).order_by(desc(models.Chat.created))
    results= await db.execute(stmt)
    kbs = results.scalars().all()
    return kbs

async def create(request: schemas.CreateChat, db: AsyncSession):
    try:
        chat = models.Chat(kb_id = request.kb_id)
        db.add(chat)
        await db.flush()
        await db.refresh(chat)
        return chat
    except SQLAlchemyError as e:
        print("SQLAlchemy error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Database error occurred.")

async def get_by_kbid(kb_id: int, db: AsyncSession):
    stmt = select(models.Chat).where(models.Chat.kb_id == kb_id)
    results = await db.execute(stmt)
    chat = results.scalars().first()
    return chat

async def get_by_id(id: uuid.UUID, db: AsyncSession):
    stmt = select(models.Chat).where(models.Chat.id == id)
    results = await db.execute(stmt)
    chat = results.scalars().first()
    return chat

async def fetch_history_by_id(id:uuid.UUID, db:AsyncSession):
    stmt = select(models.ChatMessage).options(joinedload(models.ChatMessage.tags)).filter(models.ChatMessage.chat_id == id)
    results = await db.execute(stmt)
    messages = results.unique().scalars().all()
    return messages