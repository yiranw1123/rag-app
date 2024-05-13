from starlette.requests import Request
from .api.summarizer import Summarizer
from .api.qachain import QAChain

async def get_chroma_client(request: Request):
    return request.app.state.chroma

def get_summarizer_chain():
    return Summarizer.get_summarize_chain()

def get_qa_chain():
    return QAChain.get_chain()
