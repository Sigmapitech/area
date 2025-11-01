import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routes import routers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(docs_url="/docs", lifespan=lifespan)

for route in routers:
    app.include_router(route)

if "dev" in sys.argv:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=(
            "http://localhost" "http://127.0.0.1:*"
        ),  # No comma in the tuple and it's normal
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def main():
    uvicorn.run(app, host="127.0.0.1", port=8080)
