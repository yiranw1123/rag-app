from fastapi import APIRouter, Depends,status
from sqlalchemy.orm import Session
from .. import database, schemas
from ..repository import knowledgebasefile
from typing import List

router = APIRouter(prefix="/knowledgebasefile", tags=['knowledgebasefile'])

get_db = database.get_db

@router.get('/knowledgebase/{kb_id}', response_model=List[schemas.ShowKnowledgeBaseFile])
def get_by_kbid(kb_id: int, db: Session= Depends(get_db)):
    files = knowledgebasefile.get_by_kbid(kb_id, db)
    return [schemas.ShowKnowledgeBaseFile(id=f.id, kb_id=f.kb_id, file_name=f.file_name, created=f.created, updated=f.updated) for f in files]


@router.get('/{id}', status_code=200, response_model=schemas.ShowKnowledgeBaseFile)
def get_by_id(id: int, db: Session= Depends(get_db)):
    return knowledgebasefile.get_by_id(id, db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.CreateKnowledgeBaseFile, db: Session = Depends(get_db)):
    #  1. create knowledge base in sql - return id to streamlit frontend
    id = knowledgebasefile.create(request, db)
    print(f"Created knowledgebasefile with id = {id} in knowledgebase {request.kb_id}")

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session=Depends(get_db)):
    return knowledgebasefile.delete(id, db)