from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from .. import database, schemas
from ..repository import knowledgebasefile
from typing import List
from uuid import UUID

router = APIRouter(prefix="/knowledgebasefile", tags=['knowledgebasefile'])

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowKnowledgeBaseFile])
async def all(db: AsyncSession= Depends(get_db)):
    files= await knowledgebasefile.get_all(db)
    return [schemas.ShowKnowledgeBaseFile(id=f.id, kb_id=f.kb_id, file_name=f.file_name, created=f.created, updated=f.updated) for f in files]

@router.get('/knowledgebase/{kb_id}', response_model=List[schemas.ShowKnowledgeBaseFile])
async def get_by_kbid(kb_id: int, db: AsyncSession= Depends(get_db)):
    files = await knowledgebasefile.get_by_kbid(kb_id, db)
    return [schemas.ShowKnowledgeBaseFile(id=f.id, kb_id=f.kb_id, file_name=f.file_name, created=f.created, updated=f.updated) for f in files]

@router.get('/{id}', status_code=200, response_model=schemas.ShowKnowledgeBaseFile)
async def get_by_id(id: int, db: AsyncSession= Depends(get_db)):
    return await knowledgebasefile.get_by_id(id, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(request: schemas.CreateKnowledgeBaseFile, db: AsyncSession = Depends(get_db)):
    #  1. create knowledge base in sql - return id to streamlit frontend
    id = await knowledgebasefile.create(request, db)
    print(f"Created knowledgebasefile with id = {id} in knowledgebase {request.kb_id}")
    return id

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID, db: AsyncSession=Depends(get_db)):
    await knowledgebasefile.delete(id, db)