from typing import List, Optional
from sqlalchemy import String, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Index
from datetime import datetime
from knowledgebase.database import Base
import uuid

class KnowledgeBase(Base):
    __tablename__="knowledge_base"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(255))
    embedding:Mapped[str] = mapped_column(String(30))
    description:Mapped[Optional[str]] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    updated: Mapped[datetime] = mapped_column(default=datetime.now,onupdate=datetime.now)
    files: Mapped[List["KnowledgeBaseFile"]] = relationship(cascade="all, delete, delete-orphan", lazy = "selectin")
    collection_name: Mapped[Optional[str]] = mapped_column(String(255), default= None)

    def __repr__(self) -> str:
        return f"KnowledgeBase(id={self.id!r}, name={self.name!r}, \
            embedding={self.embedding!r}, created={self.created!r}, \
            updated={self.updated!r}, collection_name={self.collection_name!r})"


class KnowledgeBaseFile(Base):
    __tablename__="knowledge_base_file"
    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True ,default=uuid.uuid4)
    kb_id:Mapped[int] = mapped_column(ForeignKey("knowledge_base.id"), index=True)
    file_name:Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    updated: Mapped[datetime] = mapped_column(default=datetime.now,onupdate=datetime.now)
    chunks = relationship("FileChunk", cascade="all, delete, delete-orphan", lazy = "selectin")

    def __repr__(self) -> str:
        return f"KnowledgeBaseFile(id={self.id!r}, file_name={self.file_name!r}, kb_id={self.kb_id!r})"

class FileChunk(Base):
    __tablename__="file_chunk"
    chunk_id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True)
    file_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("knowledge_base_file.id"))
    created: Mapped[datetime] = mapped_column(default = datetime.now)
    file = relationship("KnowledgeBaseFile", back_populates= "chunks")
Index("files_by_kb_id", KnowledgeBaseFile.kb_id)
