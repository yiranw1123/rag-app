from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database
from fastapi import status, Depends, APIRouter
from ..repository import tags
from typing import List

get_db = database.get_db

router = APIRouter(prefix="/tags", tags=['tags'])

@router.get('/{kb_id}', status_code=status.HTTP_200_OK, response_model=schemas.Tag)
async def get_by_kbid(kb_id: int, db: AsyncSession= Depends(get_db)):
    results = await tags.get_tags_for_kb(kb_id, db)
    return [schemas.Tag(id = t.id, text = t.text, embedding= t.embedding) for t in results]

async def create(requests: List[schemas.CreateTag], db: AsyncSession = Depends(get_db)):
    return await tags.create(requests, db)