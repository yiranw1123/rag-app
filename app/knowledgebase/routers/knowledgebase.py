from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Path
from .. import database, schemas
from ..repository import knowledgebase
from typing import List
from . import knowledgebasefile
from ..llm.api.fileprocesser import store_and_process_file
from sqlalchemy.ext.asyncio import AsyncSession
from ..llm.api.summarizer import get_summarizer_chain
from ..llm.store.ChromaStore import delete_collection

router = APIRouter(prefix="/knowledgebase", tags=['knowledgebase'])

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowKnowledgeBase])
async def all(db: AsyncSession= Depends(get_db)):
    data= await knowledgebase.get_all(db)
    return [schemas.ShowKnowledgeBase(id = kb.id, name=kb.name, embedding=kb.embedding, created=kb.created, updated=kb.updated, description=kb.description) for kb in data]

@router.post('/{id}/upload/', status_code=status.HTTP_201_CREATED)
async def upload_files(id: int, files:List[UploadFile] = File(...), db: AsyncSession= Depends(get_db),  summarize_chain=Depends(get_summarizer_chain)):

    for file in files:
        file_name = file.filename
        # save file info to SQL
        file_id = await knowledgebasefile.create(schemas.CreateKnowledgeBaseFile(kb_id=id, file_name=file_name), db)
        # process file and save to backend
        await store_and_process_file(file, file_id, id, summarize_chain)
        print(f"Successfully processed {file_name}")

@router.get('/{id}/files/', status_code=200, response_model=List[schemas.ShowKnowledgeBaseFile])
async def get_by_knowledgebase_id(id: int, db: AsyncSession= Depends(get_db)):
    files = await knowledgebasefile.get_by_kbid(id, db)
    return [schemas.ShowKnowledgeBaseFile(id = f.id, kb_id = f.kb_id, file_name=f.file_name, created=f.created, updated=f.updated) for f in files]

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowKnowledgeBase)
async def get_by_id(id: int, db: AsyncSession= Depends(get_db)):
    kb = await knowledgebase.get_by_id(id, db)
    return schemas.ShowKnowledgeBase(name = kb.name, id = kb.id, embedding=kb.embedding, created=kb.created, updated=kb.updated)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedKBID)
async def create(request: schemas.CreateKnowledgeBase, db: AsyncSession = Depends(get_db)):
    #  create knowledge base in sql - return id to streamlit frontend
    kb_id = await knowledgebase.create(request, db)
    print(f"Created knowledgebase with id = {kb_id}")
    return schemas.CreatedKBID(kb_id=kb_id)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession=Depends(get_db)):
    # delete chroma collection
    delete_collection(id)
    await knowledgebase.delete(id, db)