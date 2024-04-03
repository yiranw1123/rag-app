from .. import models, schemas
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_all(db: AsyncSession):
    stmt = select(models.KnowledgeBase)
    results= await db.execute(stmt)
    kbs = results.scalars().all()
    return kbs

async def get_by_id(id: int, db: AsyncSession):
    stmt = select(models.KnowledgeBase).where(models.KnowledgeBase.id == id)
    result = await db.execute(stmt)
    kb = result.scalars().first()
    if not kb:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"KnowledgeBase with the id {id} is not found.")
    return kb

async def create(reqeust: schemas.CreateKnowledgeBase, db: AsyncSession):
    kb = models.KnowledgeBase(name = reqeust.knowledgebase_name, description=reqeust.description, \
                               embedding = "embed func", collection_name=None)
    db.add(kb)
    await db.commit()
    await db.refresh(kb)
    return kb.id


async def delete(id: int, db:AsyncSession):
    stmt = select(models.KnowledgeBase).where(models.KnowledgeBase.id == id)
    result = await db.execute(stmt)
    kb = result.scalars().first()
    if not kb:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"KnowledgeBase with id {id} is not found")
    else:
        await db.delete(kb)
        await db.commit()