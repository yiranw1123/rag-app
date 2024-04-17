from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import exc
from fastapi import HTTPException

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:123@localhost/kbase"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        async with db.begin():
            try:
                yield db
                await db.commit()
            except exc.SQLAlchemyError as error:
                await db.rollback()
                raise HTTPException(status_code=500, detail=str(error))
            finally:
                await db.close()