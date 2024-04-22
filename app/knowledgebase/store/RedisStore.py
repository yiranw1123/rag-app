import asyncio
import uuid
from typing import Iterator, List
from langchain.docstore.document import Document
import json
import aioredis
from ..exceptions.RedisStoreExceptions import DocumentNotFoundException
from langchain.schema import BaseStore


class RedisStore(BaseStore[str, str]):
    def __init__(self, namespace):
        # collection_{id}:file_id
        self.namespace = namespace
        self._client = aioredis.from_url("redis://localhost:6379")

    def serialize(self, document: Document):
        return document.json()

    def deserialize(self, b_str: str):
        value = b_str.decode('utf-8')
        data = json.loads(value)
        return Document(page_content=data['page_content'],
                        metadata = data['metadata'])

    # collection_id:file_id:doc_id
    def get_namespaced_key(self, key):
        return f"{self.namespace}:{key}"

    # search collection_id:file_id in redis
    # get existing chunks in redis
    async def get_keys(self):
        match_pattern = f"{self.namespace}:*"
        all_keys = []

        cur = b"0"  # set initial cursor to 0
        while cur:
            cur, keys = await self._client.scan(cur, match=match_pattern)
            print("Iteration results:", keys)
            all_keys.extend(keys)
        return all_keys
    
    async def add_text(self, key, value):
        await self._client.set(self.get_namespaced_key(key), value)

    async def add(self, pair):
        keys = await self.get_keys()
        existed = [k for k in pair.keys() if k in keys]
        if existed:
            raise KeyError(f"key exists")
        for k,v in pair.items():
            await self.add_text(k,self.serialize(v))

    # chunk_id : document pair 
    async def mset(self, data):
        for key, val in data.items():
            await self.add({key : val})

    async def delete_keys(self, keys):
        await self._client.delete(*keys)

    async def search(self, chunk_id: str):
        try:
            res = await self._client.get(chunk_id)
            if not res:
                raise DocumentNotFoundException(chunk_id)
            return self.deserialize(res)
        except DocumentNotFoundException as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}") 
    
    async def amget(self, chunk_ids: List[str]):
        tasks = [self.search(cid) for cid in chunk_ids]
        documents = await asyncio.gather(*tasks)
        return [doc for doc in documents if doc is not None]
    
    def mget(self, chunk_ids: List[str]):
        raise NotImplementedError("Not implemented.")

    async def delete_all(self):
        keys = await self.get_keys()

        chunk_size = 100
        for i in range(0, len(keys), chunk_size):
            chunk_keys = keys[i:i+chunk_size]
            await self.delete_keys(*chunk_keys)

    async def mdelete(self, _keys):
        raise NotImplementedError("Not implemented.")
    
    async def yield_keys(self, *, prefix: str | None = None) -> Iterator | Iterator[str]:
        raise NotImplementedError("Not implemented.")