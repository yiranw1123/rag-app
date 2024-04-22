from fastapi import APIRouter, status, Depends
from .. import database, schemas
from ..dependencies import get_chroma_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain
from ..schemas import ShowChat
from typing import List
from ..repository import chat
from ..routers import knowledgebase
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/', response_model=List[ShowChat])
async def all(db: AsyncSession= Depends(get_db)):
    data = await chat.get_all(db)
    return [ShowChat(chat_name=chat.chat_name) for chat in data]


@router.get('/{id}', status_code = status.HTTP_200_OK)
async def get_retriever(id: int, chroma_client = Depends(get_chroma), db = Depends(get_db)):
    collection_name = f"{COLLECTION_PREFIX}{id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)

    # question="Where is the traveler's destination?"

    kb_details = await knowledgebase.get_by_id(id, db)
    kb_name = kb_details.name

    # chat id will be the key to redis msg store
    session_id = await chat.create(schemas.CreateChat(chat_name = kb_name, kb_id=id), db)
    
    # res = await chain.ainvoke(
    # {"input": question},
    # config={
    #     "configurable": {"session_id":session_id}
    # },  # constructs a key "abc123" in `store`.
    # )
    # print(res)

    # res = retriever.vectorstore.similarity_search(question)
    # for i in range(len(res)):
    #     print("Item ", i, ": " , res[i])

    # docs = await retriever.aget_relevant_documents(question)
    # for i in range(len(docs)):
    #     print("Doc ", i, ": " , docs[i])
    
