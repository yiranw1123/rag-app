from .. import schemas, models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from fastapi import HTTPException, status

async def create(request: schemas.CreateTag, db: AsyncSession):
    tag = models.Tag(text=request.text, embedding=request.embedding)
    db.add(tag)
    await db.flush()
    await db.refresh(tag)
    return tag

async def get_all(db: AsyncSession):
    stmt = select(models.Tag)
    results= await db.execute(stmt)
    kbs = results.scalars().all()
    return kbs


async def get_by_id(id: int, db: AsyncSession):
    stmt = select(models.Tag).where(models.Tag.id == id)
    result = await db.execute(stmt)
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"Tag with the id {id} is not found.")
    return tag

async def get_tags_for_kb(kb_id, db: AsyncSession):
    stmt = (
        select(models.Tag)
        .join(models.ChatMessage, models.Tag.chat_messages)
        .join(models.Chat, models.ChatMessage.chat)
        .join(models.KnowledgeBase, models.Chat.knowledge_base)
        .filter(models.KnowledgeBase.id == kb_id)
        .distinct()
    )
    results = await db.execute(stmt)
    tags = results.scalars().all()
    return tags
