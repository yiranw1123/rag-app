from typing import List, Optional
from sqlalchemy import String, ForeignKey, Uuid, Table, Column, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from knowledgebase.database import Base
import uuid

class KnowledgeBase(Base):
    __tablename__="knowledge_base"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255))
    embedding:Mapped[str] = mapped_column(String(30))
    description:Mapped[Optional[str]] = mapped_column(String(255))
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    files: Mapped[List["KnowledgeBaseFile"]] = relationship(cascade="all, delete, delete-orphan", lazy = "selectin")
    collection_name: Mapped[Optional[str]] = mapped_column(String(255), default= None)
    chat: Mapped["Chat"] = relationship("Chat", cascade="all, delete, delete-orphan", lazy = "selectin", back_populates="knowledge_base")

    def __repr__(self) -> str:
        return f"KnowledgeBase(id={self.id!r}, name={self.name!r}, \
            embedding={self.embedding!r}, created={self.created!r}, \
            updated={self.updated!r}, collection_name={self.collection_name!r})"

class KnowledgeBaseFile(Base):
    __tablename__="knowledge_base_file"
    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True ,default=uuid.uuid4)
    kb_id:Mapped[int] = mapped_column(ForeignKey("knowledge_base.id"), index=True)
    file_name:Mapped[str] = mapped_column(String(255))
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    chunks = relationship("FileChunk", cascade="all, delete, delete-orphan", lazy = "selectin", back_populates= "file")

    def __repr__(self) -> str:
        return f"KnowledgeBaseFile(id={self.id!r}, file_name={self.file_name!r}, kb_id={self.kb_id!r})"

class FileChunk(Base):
    __tablename__="file_chunk"
    chunk_id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True)
    file_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("knowledge_base_file.id"))
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    file = relationship("KnowledgeBaseFile", back_populates= "chunks", lazy = "selectin")

class Chat(Base):
    __tablename__ = "chat_session"
    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True ,default=uuid.uuid4)
    kb_id:Mapped[int] = mapped_column(ForeignKey("knowledge_base.id", ondelete="CASCADE"), index=True)
    knowledge_base = relationship("KnowledgeBase", back_populates="chat", single_parent=True, lazy="selectin")
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    messagesCnt: Mapped[int] = mapped_column(default=0)
    messages:Mapped[List['ChatMessage']] =  relationship(cascade="all, delete, delete-orphan", lazy ="selectin")

# Association Table for Many-to-Many relationship between ChatMessages and Tags
chat_messages_tags = Table('chat_messages_tags', Base.metadata,
    Column('chat_message_id', Uuid(as_uuid=True), ForeignKey('chat_message.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)
class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True ,default=uuid.uuid4)
    chatId: Mapped[Uuid] = mapped_column(ForeignKey("chat_session.id"), index = True)
    question: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    answer: Mapped[Text] = mapped_column(Text)
    sources = Column(JSON)
    embedding = Column(JSON)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages", lazy = "selectin")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=chat_messages_tags, back_populates="chat_messages", lazy = "selectin")

class Tag(Base):
    __tablename__ = 'tag'
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    text: Mapped[str] = mapped_column(String(255))
    embedding: Mapped[dict] = mapped_column(JSON)
    chat_messages:Mapped[list["ChatMessage"]] = relationship("ChatMessage", secondary=chat_messages_tags, back_populates="tags", lazy="selectin")
