from starlette.requests import Request
from .llm.api.summarizer import Summarizer
from .llm.api.qachain import QAChain

async def get_chroma_client(request: Request):
    return request.app.state.chroma

async def get_redis_client(request: Request):
    return request.app.state.redis

def get_summarizer_chain():
    return Summarizer.get_summarize_chain()

def get_qa_chain():
    return QAChain.get_chain()