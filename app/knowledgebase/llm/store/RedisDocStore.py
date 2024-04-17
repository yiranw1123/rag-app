import asyncio
import aioredis
import uuid
from typing import List

async def mset(collection_name_space: str, chunk_ids, text_elements, redis):
    doc_ids = [f"{collection_name_space}:{id}" for id in chunk_ids]
    data = [(doc_id, text_element) for doc_id, text_element in zip(doc_ids, text_elements)]
    try:
        await redis.amset(data)
    except Exception as e:
        print(f"Error when writing to redis: {e}")

async def delete_from_redis_collection(collection_name: str, file_id: str, chunk_ids: List[uuid.uuid4]):
    # TO DO
    redis = aioredis.from_url("redis://localhost:6379")
    keys = []
    for chunk_id in chunk_ids:
        key = f"{collection_name}:{file_id}:{chunk_id}"
        keys.append(key)
    
    await redis.delete(*keys)

def delete_collection(collectionName:str):
    # TO DO
    pass