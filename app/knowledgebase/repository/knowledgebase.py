from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    knowledge_bases = db.query(models.KnowledgeBase).all()
    return knowledge_bases

def get_by_id(id: int, db: Session):
    kb = db.query(models.KnowledgeBase).filter(models.KnowledgeBase.id == id).first()
    if not kb:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                             detail = f"KnowledgeBase with the id {id} is not found.")
    return kb

def create(reqeust: schemas.CreateKnowledgeBase, db: Session):
    kb = models.KnowledgeBase(name = reqeust.knowledgebase_name, description=reqeust.description, \
                               embedding = "embed func", collection_name=None)
    db.add(kb)
    db.commit()
    return kb.id


def delete(id: int, db:Session):
    kb = db.query(models.KnowledgeBase).filter(models.KnowledgeBase.id == id).first()
    if not kb:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"KnowledgeBase with id {id} is not found")
    db.delete(kb)
    db.commit()
    return 'done'