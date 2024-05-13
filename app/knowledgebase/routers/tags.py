from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database
from fastapi import status, Depends, APIRouter
from ..repository import tags

get_db = database.get_db

router = APIRouter(prefix="/tags", tags=['tags'])

@router.get('/{kb_id}', status_code=status.HTTP_200_OK, response_model=schemas.Tag)
async def get_by_kbid(kb_id: int, db: AsyncSession= Depends(get_db)):
    results = await tags.get_tags_for_kb(kb_id, db)
    return [schemas.Tag(id = t.id, text = t.text, embedding= t.embedding) for t in results]

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Tag)
async def create(request: schemas.CreateTag, db: AsyncSession = Depends(get_db)):
    #  create knowledge base in sql - return id to streamlit frontend
    tag = await tags.create(request, db)
    print(f"Created Tag with id = {tag.id}")
    return schemas.Tag(id = tag.id, text = tag.text, embedding= tag.embedding)