from knowledgebase.constants import CHROMA_PERSIST_DIRECTORY, COLLECTION_PREFIX, REDIS_URL
import uuid
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document

id_key = "file_id"

def add_to_collection(summaries, texts, file_id: uuid, collection_name: str, chroma_client):
    collection = chroma_client.get_or_create_collection(name = collection_name)
    doc_ids = [str(uuid.uuid4()) for _ in range(len(texts))]
    collection.add(ids=doc_ids, metadatas={id_key: str(file_id)}, documents=summaries)
    return doc_ids

def delete_from_collection(kb_id:int, file_id:uuid, chroma_client):
    # delete all chunks with given file_id
    collection = chroma_client.get_collection(name=COLLECTION_PREFIX+str(kb_id))
    collection.delete(where={'id_key': str(file_id)})

def delete_collection(kb_id: int, chroma_client):
    chroma_client.delete_collection(name=COLLECTION_PREFIX + str(kb_id))
