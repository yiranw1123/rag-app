from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi import HTTPException
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:123@localhost/kbase"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        try: # Log the session ID
            yield db
        except Exception as error:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(error))
        finally:
            await db.close()

@asynccontextmanager
async def get_db_context():
    async with SessionLocal() as db:
        try: # Log the session ID
            yield db
        except Exception as error:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(error))
        finally:
            await db.close()