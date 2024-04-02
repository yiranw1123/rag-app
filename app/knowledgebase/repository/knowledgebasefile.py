from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def get_by_id(id: int, db: Session):
    kb = db.query(models.KnowledgeBaseFile).filter(models.KnowledgeBaseFile.id == id).first()
    if not kb:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"KnowledgeBaseFile with the id {id} is not found.")
    return kb

def create(request: schemas.CreateKnowledgeBaseFile, db:Session):
    file = models.KnowledgeBaseFile(file_name=request.file_name, kb_id=request.kb_id)
    db.add(file)
    db.commit()
    return file.id

def get_by_kbid(kb_id: int, db: Session):
    files = db.query(models.KnowledgeBaseFile).filter(models.KnowledgeBaseFile.kb_id == kb_id).all()
    return files

def delete(id: int, db:Session):
    file = db.query(models.KnowledgeBaseFile).filter(models.KnowledgeBaseFile.id == id).first()
    if not file:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"KnowledgeBase File with id {id} is not found")
    db.delete(file)
    db.commit()
    return 'done'