import asyncio
import aioredis

async def mset(collection_name_space: str, chunk_ids, text_elements, redis):
    doc_ids = [f"{collection_name_space}:{id}" for id in chunk_ids]
    data = {doc_id: text_element for doc_id, text_element in zip(doc_ids, text_elements)}
    try:
        async with redis.pipeline(transaction = True) as pipe:
            for key, value in data.items():
                pipe.set(key, value.text)
            results = await pipe.execute()
        assert all(results)
    except Exception as e:
        print(f"Error during pipeline execution: {e}")

def delete_from_collection(collectionName: str):
    pass

def delete_collection(collectionName:str):
    pass