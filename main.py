from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ms_core import setup_app

from app import settings
from app.settings import db_url

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await settings.session.close()


application = FastAPI(
    title="UserMS",
    version="0.1.0",
    lifespan=lifespan
)

model_paths = ["app.models", "aerich.models"]

setup_app(
    application,
    db_url,
    Path("app") / "routers",
    model_paths
)

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": model_paths,
            "default_connection": "default",
        },
    },
}

# noinspection PyTypeChecker
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5432"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
