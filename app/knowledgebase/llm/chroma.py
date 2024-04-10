from knowledgebase.constants import CHROMA_PERSIST_DIRECTORY, COLLECTION_PREFIX, REDIS_URL
import uuid

from langchain_core.documents import Document
from langchain_community.storage import RedisStore
import chromadb

chroma_client = chromadb.PersistentClient(path= CHROMA_PERSIST_DIRECTORY)
redis_client = RedisStore(redis_url = REDIS_URL)

id_key = "doc_id"

def add_to_collection(table_summaries, text_summaries, img_summaries, texts, tables, kb_id: int, file_name:str):
    collection = chroma_client.get_or_create_collection(name = COLLECTION_PREFIX + str(kb_id))

    # Add texts
    doc_ids = [str(uuid.uuid4()) + file_name for _ in range(len(texts))]
    summary_texts = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(text_summaries)
    ]
    collection.add(ids=doc_ids, metadatas=[{id_key:doc_ids[i], "file_name": file_name} for i in range(len(summary_texts))], documents=text_summaries)
    redis_client.mset(list(zip(doc_ids, (text.encode('utf-8') for text in texts))))

    # Add tables
    table_ids = [str(uuid.uuid4()) + file_name for _ in tables]
    summary_tables = [
        Document(page_content=s, metadata={id_key: table_ids[i]})
        for i, s in enumerate(table_summaries)
    ]
    collection.add(ids=table_ids, metadatas=[{id_key:table_ids[i], "file_name": file_name} for i in range(len(summary_tables))], documents=table_summaries)
    redis_client.mset(list(zip(table_ids, (table.encode('utf-8') for table in tables))))

    # Add images
    img_ids = [str(uuid.uuid4()) + file_name for _ in img_summaries]
    summary_img = [
        Document(page_content=s, metadata={id_key: img_ids[i]})
        for i, s in enumerate(img_summaries)
    ]
    collection.add(ids=img_ids, metadatas=[{id_key:img_ids[i], "file_name": file_name} for i in range(len(summary_img))], documents=img_summaries)
    redis_client.mset(list(zip(img_ids, (img_summary.encode('utf-8') for img_summary in img_summaries))))
