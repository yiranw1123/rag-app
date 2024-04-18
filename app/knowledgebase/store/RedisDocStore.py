import asyncio
import uuid
from typing import List

async def mset(collection_name_space: str, chunk_ids, text_elements, redis):
    doc_ids = [f"{collection_name_space}:{id}" for id in chunk_ids]
    data = {doc_id: text_element for doc_id, text_element in zip(doc_ids, text_elements)}
    try:
        await redis.mset(data)
    except Exception as e:
        print(f"Error when writing to redis: {e}")

async def delete_from_redis_collection(collection_name: str, file_id: str, chunk_ids: List[uuid.uuid4], redis):
    keys = []
    for chunk_id in chunk_ids:
        key = f"{collection_name}:{file_id}:{chunk_id}"
        keys.append(key)
    try:
        await redis.delete(*keys)
    except Exception as e:
        print(f"Error when writing to redis: {e}")

async def delete_redis_collection(collection_name:str, file_ids, chunk_ids, redis):
    tasks = []
    for fid, chunks in zip(file_ids, chunk_ids):
        task = delete_from_redis_collection(collection_name, fid, chunks, redis)
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    for result in results:
        if isinstance(result, Exception):
            print(f"Error occurred: {result}")

async def delete_keys(keys, redis):
    await redis.delete(*keys)

async def search_keys(match_pattern, redis):
    all_keys = []

    async with redis.client() as conn:
        cur = b"0"  # set initial cursor to 0
        while cur:
            cur, keys = await conn.scan(cur, match=match_pattern)
            print("Iteration results:", keys)
            all_keys.extend(keys)
    return all_keys