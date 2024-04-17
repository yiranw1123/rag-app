from knowledgebase.constants import  COLLECTION_PREFIX
import uuid
import logging
from typing import List

logger = logging.getLogger(__name__)

id_key = "collection_prefix_id"

def add_to_collection(summaries, doc_ids: List[str], file_id: uuid, collection_name: str, chroma_client):
    try:
        collection = chroma_client.get_or_create_collection(name = collection_name)
        prefix_ids = [f"{collection_name}:{file_id}:{doc_id}" for doc_id in doc_ids]
        collection.add(ids=doc_ids, metadatas=[{id_key: prefix_id} for prefix_id in prefix_ids], documents=summaries)
        return doc_ids
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")

def delete_from_collection(kb_id:int, file_id:uuid, chroma_client):
    # delete all chunks with given file_id
    collection = chroma_client.get_collection(name=COLLECTION_PREFIX+str(kb_id))
    collection.delete(where={'id_key': str(file_id)})

def delete_collection(kb_id: int, chroma_client):
    chroma_client.delete_collection(name=COLLECTION_PREFIX + str(kb_id))

def get_collection(collection_name, chroma_client):
    chroma_client.get_collection(collection_name)