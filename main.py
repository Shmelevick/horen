from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from api_v1 import router as router_v1
from core.config import settings
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(users_router)


@app.get("/", response_class=HTMLResponse)
def link_to_docs():
    return '<a href="http://127.0.0.1:8000/docs"> Открыть документацию</a>'


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
