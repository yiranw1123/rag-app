from ..repository import filechunk
from .. import schemas

async def add_chunk_ids(ids, file_id, db):
    for id in ids:
        await filechunk.create(schemas.CreateFileChunk(file_id=file_id, chunk_id=id), db)