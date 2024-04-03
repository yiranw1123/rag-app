from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:123@localhost/kbase"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()