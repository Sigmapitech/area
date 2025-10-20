from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .db import init_db
from .routes import routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(docs_url="/docs", lifespan=lifespan)

for route in routers:
    app.include_router(route)

def main():
    uvicorn.run(app, host="127.0.0.1", port=8080)
