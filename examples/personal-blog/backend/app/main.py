"""Personal Blog FastAPI 入口（WI-1）"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import Base, engine
from app.api import health, posts, comments  # noqa: F401

# 显式 import 所有 ORM 模型，确保 Base.metadata 在 create_all 时能见到全部表
from app.models import post, comment, reaction  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    """启动时建表（dev 单进程；生产换 Alembic）"""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Personal Blog",
    version="0.1.0",
    description="IdeaHammer MVP demo - 按方法论从零到一真跑",
    lifespan=lifespan,
)
app.include_router(health.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(comments.router, prefix="/api")