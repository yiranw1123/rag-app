from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from knowledgebase import models
from knowledgebase.routers import knowledgebase, knowledgebasefile
from knowledgebase.database import engine

async def onStart():
    async with engine.begin() as conn:
        #await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await onStart()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(knowledgebase.router)
app.include_router(knowledgebasefile.router)

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