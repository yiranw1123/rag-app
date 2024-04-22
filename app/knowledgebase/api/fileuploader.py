from .fileprocesser import save_file, parse_pdf, summarize, clear_file_dir, clear_img_dir
from ..repository import knowledgebase
from ..routers import knowledgebasefile
from fastapi import UploadFile
import uuid
from .. import schemas
from ..routers.filechunk import add_chunk_ids
from ..constants import COLLECTION_PREFIX
from typing import List
from ..store.ChromaStore import delete_from_collection,add_to_collection
from ..store.RedisStore import RedisStore
from ..store.utils.RedisStoreUtils import handle_file_delete_in_redis
import logging
from langchain.docstore.document import Document
from itertools import chain


logger = logging.getLogger(__name__)


async def handle_file_upload(id, file:UploadFile, db, chroma, summarize_chain):
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

    combined_ids = list(chain(text_ids, table_ids, img_ids))
    combined_summaries = list(chain(text_summaries, table_summaries, img_summaries))
    if(len(combined_ids) != len(combined_summaries)):
        raise Exception(f"Number of ids {len(combined_ids)} and {len(combined_summaries)} doesn't match")

    await add_chunk_ids(combined_ids, file_id, db)

    collection_name = f"{COLLECTION_PREFIX}{str(id)}"
    await save_to_chroma(collection_name, file_id, chroma, combined_ids, combined_summaries)
    
    # create redis client for adding file with file_id to redis
    redis_namespace = f"{collection_name}:{file_id}"
    redis_client = RedisStore(redis_namespace)
    await save_to_redis(redis_client, combined_ids, combined_summaries)

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

async def handle_redis_rollback(kb_id, processed:List[str]):
    for fid in processed:
        try:
            await handle_file_delete_in_redis(kb_id, fid)
            logger.info(f"Redis - Successfully rolled back file with id {fid} in knowledge base{kb_id}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {str(e)}")

async def save_to_chroma(collection_name: str, file_id: uuid, chroma_client,
                        combined_ids, combined_summaries):
    try:
        add_to_collection(combined_summaries, combined_ids, file_id, collection_name, chroma_client)
        print(f"Successfully processed {len(combined_ids)} summaries")
    except Exception as e:
        logger.exception(f"An unexpected exception occured: {e}")
    
async def save_to_redis(redis_client, combined_ids, combined_summaries):
    try:
        data = await create_documents(combined_ids, combined_summaries)
        await redis_client.mset(data)
    except Exception as e:
        logger.exception(f"An unexpected exception occured: {e}")        

# return a dictionary of chunk_id: document
async def create_documents(text_ids, text_elements):
    dict = {}

    for id, element in zip(text_ids, text_elements):
      dict[id] = Document(page_content=element, metadata={"doc_id": id})

    return dict