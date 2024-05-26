from pydantic import BaseModel, UUID4, Field, validator
from datetime import datetime
from typing import Any, List, Dict, Optional
import json

class ShowKnowledgeBase(BaseModel):
    name: str
    id: int
    embedding: str
    created: datetime
    updated: datetime
    description: Optional[str] = None
class ShowKnowledgeBaseFile(BaseModel):
    id: UUID4
    kb_id: int
    file_name: str
    created: datetime
    updated:datetime
    chunks:List[UUID4]
class CreateKnowledgeBase(BaseModel):
    knowledgebase_name: str
    description: Optional[str] = None
class CreatedKBID(BaseModel):
    kb_id: int
class CreateKnowledgeBaseFile(BaseModel):
    kb_id: int
    file_name: str
class CreateFileChunk(BaseModel):
    chunk_id: UUID4
    file_id: UUID4

class ShowChat(BaseModel):
    id: UUID4

class CreateChat(BaseModel):
    kb_id: int

class CreateTag(BaseModel):
    text: str
    embedding: List

class Tag(BaseModel):
    id: int
    text: str
    embedding: List = None


class TagsDict(BaseModel):
    matched_tag: Optional[List[Tag]] = None
    new_tags: Optional[List[CreateTag]] = None

class CreateChatMessage(BaseModel):
    id: UUID4
    chat_id: UUID4 = Field(alias='chat_id')
    timestamp:str
    question: str
    answer: str
    sources: dict
    embedding: list
    tags: TagsDict = None


class ChatMessage(BaseModel):
    id: UUID4
    chat_id: UUID4
    question: str
    answer: str
    sources: str
    tags_list: Optional[str] = None
    timestamp: str

    @validator('tags_list', pre=True, always=True)
    def serialize_tags_list(cls, v):
        if isinstance(v, list):
            return json.dumps([tag.dict() for tag in v])
        return v

class Element(BaseModel):
    type: str
    text: Any

class Document(BaseModel):
    page_content: str
    doc_id: str

class DocumentList(BaseModel):
    documents: List[Document]