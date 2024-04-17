from .. import models, schemas
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from typing import List

async def create(request: schemas.CreateFileChunk, db: AsyncSession):
    chunk = models.FileChunk(chunk_id=request.chunk_id, file_id = request.file_id)
    db.add(chunk)
    await db.flush()
    await db.refresh(chunk)
    return chunk.chunk_id

async def get_by_file_id(file_id: uuid, db: AsyncSession):
    stmt = select(models.FileChunk).where(models.FileChunk.file_id == file_id)
    results = await db.execute(stmt)
    files = results.scalars().all()
    return files
