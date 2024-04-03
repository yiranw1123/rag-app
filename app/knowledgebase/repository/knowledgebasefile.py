from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import models, schemas
from fastapi import HTTPException, status

async def get_all(db: AsyncSession):
    stmt = select(models.KnowledgeBaseFile)
    results= await db.execute(stmt)
    kb_files = results.scalars().all()
    return kb_files

async def get_by_id(id: int, db: AsyncSession):
    stmt = select(models.KnowledgeBaseFile).where(models.KnowledgeBaseFile.id == id)
    result = await db.execute(stmt)
    kb_file =  result.scalars().first()
    if not kb_file:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"KnowledgeBaseFile with the id {id} is not found.")
    return kb_file

async def create(request: schemas.CreateKnowledgeBaseFile, db:AsyncSession):
    file = models.KnowledgeBaseFile(file_name=request.file_name, kb_id=request.kb_id)
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file.id

async def get_by_kbid(kb_id: int, db: AsyncSession):
    stmt = select(models.KnowledgeBaseFile).where(models.KnowledgeBaseFile.kb_id == kb_id)
    results = await db.execute(stmt)
    files = results.scalars().all()
    return files

async def delete(id: int, db:AsyncSession):
    stmt = select(models.KnowledgeBaseFile).where(models.KnowledgeBaseFile.id == id)
    result = await db.execute(stmt)
    file = result.scalars().first()
    if not file:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"KnowledgeBase File with id {id} is not found")
    else:
        await db.delete(file)
        await db.commit()