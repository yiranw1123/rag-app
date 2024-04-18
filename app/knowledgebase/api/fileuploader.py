from .fileprocesser import save_file, parse_pdf, summarize, clear_file_dir, clear_img_dir
from ..repository import knowledgebase
from ..routers import knowledgebasefile
from fastapi import UploadFile
import uuid
from .. import schemas
from ..routers.filechunk import add_chunk_ids
from ..constants import COLLECTION_PREFIX
from typing import List
from ..store.ChromaStore import delete_from_collection
from ..store.RedisDocStore import search_keys, delete_keys
import logging
from ..routers import knowledgebasefile
from ..store.ChromaStore import add_to_collection
from ..store.RedisDocStore import mset
import asyncio

logger = logging.getLogger(__name__)


async def handle_file_upload(id, file:UploadFile, db, chroma, redis, summarize_chain):
    file_name = file.filename
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

    ids = text_ids
    ids.extend(table_ids)
    ids.extend(img_ids)

    await add_chunk_ids(ids, file_id, db)

    collection_name = f"{COLLECTION_PREFIX}{str(id)}"
    redis_namespace = f"{collection_name}:{file_id}"

    await save_to_chroma(collection_name, file_id, chroma, text_summaries, text_ids, table_summaries, table_ids, img_summaries, img_ids)
    await save_to_redis(redis_namespace, redis, text_elements, text_ids, table_elements, table_ids, img_summaries, img_ids)

    await clear_img_dir(file_id=file_id)
    await clear_file_dir(file_id=file_id)

    return file_id

def handle_chroma_rollback(kb_id, processed:List[str], chroma):
    for fid in processed:
        try:
            delete_from_collection(kb_id, fid, chroma)
            logger.info(f"Chroma - Successfully rolled back file with id {fid} in knowledge base{kb_id}")

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {str(e)}")

async def handle_redis_rollback(kb_id, processed:List[str], redis):
    for fid in processed:
        try:
            match_pattern = f"{COLLECTION_PREFIX}{kb_id}:{fid}:*"
            keys = await search_keys(match_pattern, redis)
            await delete_keys(keys, redis)
            logger.info(f"Redis - Successfully rolled back file with id {fid} in knowledge base{kb_id}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {str(e)}")

async def save_to_chroma(collection_name: str, file_id: uuid, chroma_client,
                        text_summaries, text_ids, table_summaries, table_ids, img_summaries, img_ids):
    try:
        if text_summaries:
            add_to_collection(text_summaries, text_ids, file_id, collection_name, chroma_client)
            print(f"processed {len(text_summaries)} text summaries")
        if table_summaries:
            add_to_collection(table_summaries, table_ids, file_id, collection_name, chroma_client)
            print(f"processed {len(table_summaries)} table summaries")
        if img_summaries:
            add_to_collection(img_summaries, img_ids, file_id, collection_name, chroma_client)
            print(f"processed {len(img_summaries)} image summaries")
    except Exception as e:
        logger.exception(f"An unexpected exception occured: {e}")
    
async def save_to_redis(redis_namespace: str, redis_client,
                        text_elements, text_ids, table_elements, table_ids, img_summaries, img_ids):
    try:
        if text_elements:
            await mset(redis_namespace, text_ids, [text_element.text for text_element in text_elements], redis_client)
        if table_elements:
            await mset(redis_namespace, table_ids, [table_element.text for table_element in table_elements],redis_client)
        if img_summaries:
            await mset(redis_namespace, img_ids, img_summaries,redis_client)
    except Exception as e:
        logger.exception(f"An unexpected exception occured: {e}")        
