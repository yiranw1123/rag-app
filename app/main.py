from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from knowledgebase import models
from knowledgebase.routers import knowledgebase, knowledgebasefile, chat, chatmessage, tags
from knowledgebase.database import engine
import chromadb
from dotenv import load_dotenv
import os
import logging
from alembic.config import Config
from alembic import command

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def onStart(app: FastAPI):
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    await init_db()

    app.state.chroma = chromadb.HttpClient(host="localhost", port=8080)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

async def onShutdown(app:FastAPI):
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    await onStart(app)
    try:
        yield
    finally:
        await onShutdown(app)

app = FastAPI(lifespan=lifespan)

origins=[
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledgebase.router)
app.include_router(knowledgebasefile.router)
app.include_router(chat.router)
app.include_router(chatmessage.router)
app.include_router(tags.router)
app.websocket("/chat/{id}/ws")(chat.post)

# @app.middleware("http")
# async def log_request(request: Request, call_next):
#     response = await call_next(request)
#     print(f"Request headers: {request.headers}")
#     print(f"Response headers: {response.headers}")
#     return response