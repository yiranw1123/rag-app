from fastapi import APIRouter, Depends, status, File, UploadFile
from .. import database, schemas
from ..repository import knowledgebase
from typing import List
from . import knowledgebasefile
from ..api.fileuploader import handle_file_upload, handle_chroma_rollback, handle_redis_rollback
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_summarizer_chain
from ..store.ChromaStore import delete_collection
from ..store.RedisDocStore import delete_redis_collection
from ..dependencies import get_chroma_client, get_redis_client
import logging
from ..constants import COLLECTION_PREFIX

router = APIRouter(prefix="/knowledgebase", tags=['knowledgebase'])

get_db = database.get_db
get_chroma = get_chroma_client
get_redis = get_redis_client

logger = logging.getLogger(__name__)


@router.get('/', response_model=List[schemas.ShowKnowledgeBase])
async def all(db: AsyncSession= Depends(get_db)):
    data = await knowledgebase.get_all(db)
    return [schemas.ShowKnowledgeBase(id = kb.id, name=kb.name, embedding=kb.embedding, created=kb.created, updated=kb.updated, description=kb.description) for kb in data]

@router.post('/{id}/upload/', status_code=status.HTTP_201_CREATED)
async def upload_files(id: int, files:List[UploadFile] = File(...),
                        db: AsyncSession= Depends(get_db),  summarize_chain=Depends(get_summarizer_chain),
                        chroma=Depends(get_chroma), redis=Depends(get_redis)):
    processed = []
    for file in files:
        try:
            file_id = await handle_file_upload(id, file, db, chroma, redis, summarize_chain)
            processed.append(str(file_id))
            raise Exception("test roll back")
            print(f"Successfully processed {file.filename}")
        except Exception as e:
            logger.exception(f"Exception occured {e}")
            handle_chroma_rollback(id, processed, chroma)
            await handle_redis_rollback(id, processed, redis)
            raise

@router.get('/{id}/files/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowKnowledgeBaseFile])
async def get_by_knowledgebase_id(id: int, db: AsyncSession= Depends(get_db)):
    files = await knowledgebasefile.get_by_kbid(id, db)
    return files

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
async def delete(id: int, db: AsyncSession=Depends(get_db), chroma_client = Depends(get_chroma), redis = Depends(get_redis)):
    # delete chroma collection
    delete_collection(id, chroma_client)
    files = await knowledgebasefile.get_by_kbid(id, db)
    file_ids = [file.id for file in files]
    chunk_ids = [file.chunks for file in files]
    assert(len(chunk_ids) ==  len(files))
    # delete from redis
    await delete_redis_collection(collection_name=f"{COLLECTION_PREFIX}{id}",file_ids = file_ids, chunk_ids = chunk_ids, redis=redis)
    await knowledgebase.delete(id, db)