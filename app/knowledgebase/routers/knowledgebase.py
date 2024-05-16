from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException, Form
from .. import database, schemas
from ..repository import knowledgebase
from typing import List, Optional
from . import knowledgebasefile
from ..api.fileuploader import handle_file_uploads
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_summarizer_chain
from ..store.ChromaStore import delete_collection
from ..store.utils.RedisStoreUtils import handle_multiple_file_delete_in_redis
from ..dependencies import get_chroma_client
import logging

router = APIRouter(prefix="/knowledgebase", tags=['knowledgebase'])

get_db = database.get_db
get_chroma = get_chroma_client

logger = logging.getLogger(__name__)


@router.get('/', response_model=List[schemas.ShowKnowledgeBase])
async def all(db: AsyncSession= Depends(get_db)):
    data = await knowledgebase.get_all(db)
    return [schemas.ShowKnowledgeBase(id = kb.id, name=kb.name, embedding=kb.embedding, created=kb.created, updated=kb.updated, description=kb.description) for kb in data]

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedKBID)
async def create(knowledgebase_name: str = Form(...), description: Optional[str] = Form(None),
                files: List[UploadFile] = File(...), db: AsyncSession= Depends(get_db),
                summarize_chain=Depends(get_summarizer_chain), chroma=Depends(get_chroma)):
    async with db.begin():
        kb_id = await knowledgebase.create(schemas.CreateKnowledgeBase(knowledgebase_name=knowledgebase_name, description=description), db)
        await handle_file_uploads(kb_id=kb_id, files=files, db=db, chroma=chroma, summarize_chain = summarize_chain)
        print(f"Created knowledgebase with id = {kb_id}")
        return schemas.CreatedKBID(kb_id=kb_id)

@router.post('/{kb_id}/upload/', status_code=status.HTTP_201_CREATED)
async def upload_files(kb_id: Optional[int] = None, files: List[UploadFile] = File(...),
                                    db: AsyncSession= Depends(get_db), chroma=Depends(get_chroma),
                                    summarize_chain=Depends(get_summarizer_chain)):
    pass

@router.get('/{id}/files/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowKnowledgeBaseFile])
async def get_by_knowledgebase_id(id: int, db: AsyncSession= Depends(get_db)):
    files = await knowledgebasefile.get_by_kbid(id, db)
    return files

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowKnowledgeBase)
async def get_by_id(id: int, db: AsyncSession= Depends(get_db)):
    kb = await knowledgebase.get_by_id(id, db)
    return schemas.ShowKnowledgeBase(name = kb.name, id = kb.id, embedding=kb.embedding,
                                      created=kb.created, updated=kb.updated, description=kb.description)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession=Depends(get_db), chroma_client = Depends(get_chroma)):
    # delete chroma collection
    delete_collection(id, chroma_client)
    files = await knowledgebasefile.get_by_kbid(id, db)
    file_ids = [file.id for file in files]
    chunk_ids = [file.chunks for file in files]
    assert(len(chunk_ids) ==  len(files))
    # delete from redis
    await handle_multiple_file_delete_in_redis(id, file_ids)
    await knowledgebase.delete(id, db)