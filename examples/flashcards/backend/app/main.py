from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, cards
from app.db import Base, engine
from app.models import Card  # noqa: F401  确保模型被注册


@asynccontextmanager
async def lifespan(_: FastAPI):
    """启动时建表（开发用，生产应用 Alembic 迁移）"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="IdeaHammer Flashcards", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(cards.router, prefix="/api")
