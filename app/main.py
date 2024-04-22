from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from knowledgebase import models
from knowledgebase.routers import knowledgebase, knowledgebasefile, chat
from knowledgebase.database import engine
import chromadb
from dotenv import load_dotenv
import aioredis
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def onStart(app: FastAPI):
    async with engine.begin() as conn:

        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

    app.state.chroma = chromadb.HttpClient(host="localhost", port=8080)

    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

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
app.include_router(knowledgebase.router)
app.include_router(knowledgebasefile.router)
app.include_router(chat.router)

origins=[
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)