from .. import schemas, models
from sqlalchemy.ext.asyncio import AsyncSession
from . import tags
import json
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from sqlalchemy import select


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

        message = models.ChatMessage(id = request.id, chat_id = request.chat_id, question = request.question,
                                    answer = request.answer, sources = request.sources, timestamp = request.timestamp,
                                    embedding = embedding, tags=tags_to_add)
        db.add(message)
        await db.flush()
        await db.refresh(message)

        # update messagesCnt for chat_session
        chat_id = message.chat_id
        result = await db.execute(select(models.Chat).filter(models.Chat.id == chat_id))
        chat = result.scalar()
        if chat:
            chat.messagesCnt += 1
        else:
            raise HTTPException(status_code=404, detail=f"chat_session with id{chat_id} not found")
        return message
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Data integrity error.")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error.{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))