from pydantic import BaseModel,UUID4
from datetime import datetime
from typing import Any, List

class ShowKnowledgeBase(BaseModel):
    name: str
    id: int
    embedding: str
    created: datetime
    updated: datetime
    description: str

class ShowKnowledgeBaseFile(BaseModel):
    id: UUID4
    kb_id: int
    file_name: str
    created: datetime
    updated:datetime
    chunks:List[UUID4]

class CreateKnowledgeBase(BaseModel):
    knowledgebase_name: str
    description: str | None = None

class CreatedKBID(BaseModel):
    kb_id: int

class CreateKnowledgeBaseFile(BaseModel):
    kb_id: int
    file_name: str

class CreateFileChunk(BaseModel):
    chunk_id: UUID4
    file_id: UUID4

class ShowChat(BaseModel):
    chat_name: str

class CreateChat(BaseModel):
    chat_name: str
    kb_id: int

class Element(BaseModel):
    type: str
    text: Any