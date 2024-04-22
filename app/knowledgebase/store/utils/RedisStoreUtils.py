from .. import RedisStore
from typing import List
import uuid
from ...constants import COLLECTION_PREFIX
import asyncio

# delete all chunks for file_id with kb_id
async def handle_file_delete_in_redis(kb_id: int, file_id:str):
    redis_namespace = f"{COLLECTION_PREFIX}{kb_id}:{file_id}"
    redis = RedisStore(redis_namespace)
    keys = await redis.get_keys()

async def handle_multiple_file_delete_in_redis(kb_id: int, file_ids: List[str]):
    for fid in file_ids:
        tasks = [handle_file_delete_in_redis(kb_id, fid)]
        await asyncio.gather(tasks)