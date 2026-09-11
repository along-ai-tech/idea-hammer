from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, cards

app = FastAPI(title="IdeaHammer Flashcards", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(cards.router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """启动时建表（开发用，生产应用 Alembic 迁移）"""
    from app.db import Base, engine
    from app.models import Card  # noqa: F401
    Base.metadata.create_all(bind=engine)
