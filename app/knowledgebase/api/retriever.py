from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from ..store.RedisStore import RedisStore
from langchain.storage._lc_store import create_kv_docstore

async def create_retriever(collection_name, chroma_client):
    id_key = "collection_prefix_id"
    vectorstore = Chroma(
        client = chroma_client,
        collection_name = collection_name,
        embedding_function = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")
    )

    retriever = MultiVectorRetriever(
        vectorstore= vectorstore,
        docstore=RedisStore(namespace=collection_name), 
        id_key = id_key
    )
    return retriever