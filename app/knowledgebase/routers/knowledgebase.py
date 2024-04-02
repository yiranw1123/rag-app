from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Path
from sqlalchemy.orm import Session
from .. import database, schemas
from ..repository import knowledgebase
from typing import List, Annotated
from . import knowledgebasefile
from app.llm.process_file import process_pdf_and_summarize_elements
import os
from ..save_file import save_file
from ..constants import UPLOADED_FILES_DIR
from app.llm.vectorstore import add_to_collection

router = APIRouter(prefix="/knowledgebase", tags=['knowledgebase'])

get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowKnowledgeBase])
def all(db: Session= Depends(get_db)):
    data= knowledgebase.get_all(db)
    return [schemas.ShowKnowledgeBase(id = kb.id, name=kb.name, embedding=kb.embedding, created=kb.created, updated=kb.updated) for kb in data]

@router.post('/{id}/upload/', status_code=status.HTTP_201_CREATED)
def upload_files(id: int, files:List[UploadFile] = File(...), db: Session= Depends(get_db)):

    for file in files:
        file_name = file.filename
        # save file info to SQL
        knowledgebasefile.create(schemas.CreateKnowledgeBaseFile(kb_id=id, file_name=file_name), db)
        # save uploaded file to local dir
        #save_file(file=file)
        #  2. process files and create embedding
        #table_summaries, text_summaries, img_summaries, texts, tables = process_pdf_and_summarize_elements(filename=file_name)
        #  3 create vector db with collection name collection_{knowledge_base_id}
        #add_to_collection(table_summaries, text_summaries, img_summaries, texts, tables, kb_id=id, file_name=file_name)
        #  4. persist file chunks to redis with namespace prefix collection_{knowledge_base_id}
        print(f"received files to upload to knowledgebase id: {id}")


@router.get('/{id}/files/', status_code=200, response_model=List[schemas.ShowKnowledgeBaseFile])
def get_by_knowledgebase_id(id: int, db: Session= Depends(get_db)):
    files = knowledgebasefile.get_by_kbid(id, db)
    return [schemas.ShowKnowledgeBaseFile(id = f.id, kb_id = f.kb_id, file_name=f.file_name, created=f.created, updated=f.updated) for f in files]

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowKnowledgeBase)
def get_by_id(id: int, db: Session= Depends(get_db)):
    kb = knowledgebase.get_by_id(id, db)
    return schemas.ShowKnowledgeBase(name = kb.name, id = kb.id, embedding=kb.embedding, created=kb.created, updated=kb.updated)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedKBID)
def create(request: schemas.CreateKnowledgeBase, db: Session = Depends(get_db)):
    #  create knowledge base in sql - return id to streamlit frontend
    kb_id = knowledgebase.create(request, db)
    print(f"Created knowledgebase with id = {kb_id}")
    return schemas.CreatedKBID(kb_id=kb_id)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session=Depends(get_db)):
    return knowledgebase.delete(id, db)