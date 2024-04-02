from fastapi import FastAPI
from knowledgebase import models
from knowledgebase.database import engine
from knowledgebase.routers import knowledgebase, knowledgebasefile

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(knowledgebase.router)
app.include_router(knowledgebasefile.router)