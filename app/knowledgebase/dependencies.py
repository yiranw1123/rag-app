from starlette.requests import Request

async def get_chroma_client(request: Request):
    return request.app.state.chroma

async def get_redis_client(request: Request):
    return request.app.state.redis