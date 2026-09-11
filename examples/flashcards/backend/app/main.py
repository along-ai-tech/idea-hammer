from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api import health, cards, study
from app.db import Base, engine
from app.models import Card  # noqa: F401  确保模型被注册


def _ensure_card_columns():
    """增量加列：dev 环境的临时 migration，生产用 Alembic
    
    检查现有 cards 表的列，对比 ORM 模型，缺啥补啥。"""
    inspector = inspect(engine)
    if "cards" not in inspector.get_table_names():
        return  # 新库，create_all 会建完整 schema
    existing = {c["name"] for c in inspector.get_columns("cards")}
    additions = [
        ("repetitions", "INTEGER DEFAULT 0 NOT NULL"),
        ("interval", "INTEGER DEFAULT 0 NOT NULL"),
        ("easiness_factor", "FLOAT DEFAULT 2.5 NOT NULL"),
        ("due_at", "DATETIME"),
        ("last_reviewed_at", "DATETIME"),
    ]
    with engine.begin() as conn:
        for col_name, col_def in additions:
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE cards ADD COLUMN {col_name} {col_def}"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    """启动时建表 + 增量加列（开发用，生产应用 Alembic 迁移）"""
    Base.metadata.create_all(bind=engine)
    _ensure_card_columns()
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
app.include_router(study.router, prefix="/api")
