from .. import schemas, models, database
from sqlalchemy.ext.asyncio import AsyncSession
from . import tags
import json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import asyncio

get_db = database.get_db

async def create(request: schemas.CreateChatMessage, db: AsyncSession):
    try:
        embedding = json.dumps(request.embedding)
        tags_to_add = []
        if request.tags['matches']:
            matched_tags = [await tags.get_by_id(tagModel.id, db)for tagModel in request.tags['matches']]
            tags_to_add.extend(matched_tags)
        if request.tags['new_tags']:
            new_tags = [await tags.create(tagModel, db) for tagModel in request.tags['new_tags']]
            tags_to_add.extend(new_tags)

        message = models.ChatMessage(chatId = request.chatId, question = request.question,
                                    answer = request.answer, sources = request.sources, 
                                    embedding = embedding, tags=tags_to_add)
        db.add(message)
        await db.flush()
        await db.refresh(message)
        return message
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Data integrity error.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))