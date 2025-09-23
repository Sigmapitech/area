from contextlib import asynccontextmanager
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import routers
from .db import init_db

app = FastAPI(docs_url="/docs")

for router in routers:
    app.include_router(router, prefix="/api")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


if "dev" in sys.argv:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=("http://localhost" "http://127.0.0.1:*"),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
