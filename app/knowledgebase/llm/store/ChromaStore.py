from knowledgebase.constants import CHROMA_PERSIST_DIRECTORY, COLLECTION_PREFIX, REDIS_URL
import uuid
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
from langchain_community.storage import RedisStore
import chromadb

id_key = "file_id"

class ChromaStore(object):
    _client = None
    
    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = chromadb.PersistentClient(path= CHROMA_PERSIST_DIRECTORY)
        return cls._client
    
def add_to_collection(summaries, texts, file_id: uuid, kb_id: int):
    client = ChromaStore.get_client()
    collection = client.get_or_create_collection(name = COLLECTION_PREFIX + str(kb_id))
    doc_ids = [str(uuid.uuid4()) for _ in range(len(texts))]
    collection.add(ids=doc_ids, metadatas={id_key: str(file_id)}, documents=summaries)

def delete_from_collection(kb_id:int, file_id:uuid):
    # delete all chunks with given file_id
    client = ChromaStore.get_client()
    collection = client.get_collection(name=COLLECTION_PREFIX+str(kb_id))
    collection.delete(where={'id_key': str(file_id)})

def delete_collection(kb_id: int):
    client = ChromaStore.get_client()
    client.delete_collection(name=COLLECTION_PREFIX + str(kb_id))
