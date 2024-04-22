from fastapi import APIRouter, status, Depends
from .. import database
from ..dependencies import get_chroma_client
from ..api.retriever import create_retriever
from ..constants import COLLECTION_PREFIX
from ..api.qachain import QAChain
import uuid



router = APIRouter(prefix="/chat", tags = ['chat'])

get_db = database.get_db
get_chroma = get_chroma_client

@router.get('/{id}', status_code = status.HTTP_200_OK)
async def get_retriever(id: int, chroma_client = Depends(get_chroma)):
    collection_name = f"{COLLECTION_PREFIX}{id}"
    retriever = await create_retriever(collection_name, chroma_client)
    chain = QAChain.get_chain(retriever)

    question="Where is the traveler's destination?"

    session_id = str(uuid.uuid4())
    
    res = await chain.ainvoke(
    {"input": question},
    config={
        "configurable": {"session_id":session_id}
    },  # constructs a key "abc123" in `store`.
    )
    print(res)

    # res = retriever.vectorstore.similarity_search(question)
    # for i in range(len(res)):
    #     print("Item ", i, ": " , res[i])

    # docs = await retriever.aget_relevant_documents(question)
    # for i in range(len(docs)):
    #     print("Doc ", i, ": " , docs[i])
    
