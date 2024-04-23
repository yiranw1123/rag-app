from fastapi import APIRouter, status, Depends
from .. import database, schemas
from ..dependencies import get_chroma_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain
from typing import List
from ..repository import chat
from ..routers import knowledgebase
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/', response_model=List[schemas.ShowChat])
async def all(db: AsyncSession= Depends(get_db)):
    data = await chat.get_all(db)
    return [schemas.ShowChat(chat_name=chat.chat_name, id = chat.id, kb_id=chat.kb_id) for chat in data]

@router.get('/kb_id/{kb_id}', response_model=schemas.ShowChat)
async def get_by_kbid(kb_id:int, db: AsyncSession= Depends(get_db)):
    c = await chat.get_by_kbid(kb_id, db)
    if not c:
        kb_details = await knowledgebase.get_by_id(kb_id, db)
        kb_name = kb_details.name

        # chat id will be the key to redis msg store
        c = await chat.create(schemas.CreateChat(chat_name = kb_name, kb_id=kb_id), db)
    return schemas.ShowChat(chat_name=c.chat_name, kb_id= c.kb_id, id = c.id)


@router.post('/{id}')
# id is the uuid for chat session with kb_id
async def post(request:schemas.ChatMessage, chroma_client = Depends(get_chroma)):
    chain = await get_retriever(kb_id, chroma_client, db)
    res = await chain.ainvoke(
        {"input": request.msg},
        config={
            "configurable": {"session_id":id}
    })
    return res


@router.get('/{kb_id}', status_code = status.HTTP_200_OK)
async def get_retriever(kb_id: int, chroma_client = Depends(get_chroma), db = Depends(get_db)):
    #check if a session with this kb_id already exists, if so load the history
    collection_name = f"{COLLECTION_PREFIX}{kb_id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)
    return chain

    # question="Where is the traveler's destination?"
    
    # res = await chain.ainvoke(
    # {"input": question},
    # config={
    #     "configurable": {"session_id":session_id}
    # }
    # )
    # print(res)

    # res = retriever.vectorstore.similarity_search(question)
    # for i in range(len(res)):
    #     print("Item ", i, ": " , res[i])

    # docs = await retriever.aget_relevant_documents(question)
    # for i in range(len(docs)):
    #     print("Doc ", i, ": " , docs[i])
    
