from fastapi import APIRouter, Depends, status, File, UploadFile
from .. import database, schemas
from ..repository import knowledgebase, filechunk
from typing import List
from . import knowledgebasefile
from ..llm.api.fileprocesser import save_file, parse_pdf, summarize, save_to_chroma, save_to_redis, clear_file_dir, clear_img_dir
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_summarizer_chain
from ..llm.store.ChromaStore import delete_collection
from ..dependencies import get_chroma_client, get_redis_client
import logging
import uuid
from .filechunk import add_chunk_ids
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

    for file in files:
        try:
            file_name = file.filename
            logger.info(f"Ready to process {file_name}")
            kb_exists = await knowledgebase.get_by_id(id, db)
            if not kb_exists:
                raise ValueError("KnowledgeBase ID does not exist")
            # save file info to SQL
            file_id = await knowledgebasefile.create(schemas.CreateKnowledgeBaseFile(kb_id=id, file_name=file_name), db)
            # process file and save to backend
            stored_file_name = await save_file(file, file_id)
            table_elements, text_elements = await parse_pdf(stored_file_name, file_id)
            text_summaries, table_summaries, img_summaries = await summarize(text_elements, table_elements, file_id, summarize_chain)
            
            text_ids = [str(uuid.uuid4()) for _ in range(len(text_summaries))]
            table_ids = [str(uuid.uuid4()) for _ in range(len(table_summaries))]
            img_ids = [str(uuid.uuid4()) for _ in range(len(img_summaries))]

            text_ids.extend(table_ids)
            text_ids.extend(img_ids)

            await add_chunk_ids(text_ids, file_id, db)

            collection_name = f"{COLLECTION_PREFIX}{str(id)}"
            redis_namespace = f"{collection_name}:{file_id}"
            await save_to_chroma(collection_name, file_id, chroma, text_summaries, text_ids, table_summaries, table_ids, img_summaries, img_ids)
            await save_to_redis(redis_namespace, redis, text_elements, text_ids, table_elements, table_ids, img_summaries, img_ids)

            await clear_img_dir(file_id=file_id)
            await clear_file_dir(file_id=file_id)

            print(f"Successfully processed {file_name}")
        except Exception as e:
            logger.exception(f"Exception occured {e}")
            raise

@router.get('/{id}/files/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowKnowledgeBaseFile])
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
async def delete(id: int, db: AsyncSession=Depends(get_db), chroma_client = Depends(get_chroma)):
    # delete chroma collection
    delete_collection(id,chroma_client)
    await knowledgebase.delete(id, db)