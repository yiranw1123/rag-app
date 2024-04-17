from fastapi import APIRouter, status, Depends
from .. import database
from ..dependencies import get_chroma_client, get_redis_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain


router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client
get_redis = get_redis_client

@router.get('/{id}', status_code = status.HTTP_200_OK)
async def get_retriever(id: int, chroma_client = Depends(get_chroma), redis_client = Depends(get_redis)):
    collection_name = f"{COLLECTION_PREFIX}{id}"
    retriever = await create_retriever(collection_name, chroma_client, redis_client)
    chain = QAChain.get_chain(retriever)

    question="wwhen is taylor's birthday?"

    res = retriever.vectorstore.similarity_search(question)
    for i in range(len(res)):
        print("Item ", i, ": " , res[i])

    docs = retriever.get_relevant_documents(question)
    for i in range(len(docs)):
        print("Doc ", i, ": " , docs[i])
    
