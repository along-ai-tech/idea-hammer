"""SQLAlchemy 引擎 + Base + get_db 依赖"""
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./personal_blog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)


# SQLite 默认 PRAGMA foreign_keys=OFF，必须每个 connection 显式开启，
# 否则 ON DELETE CASCADE 在 DDL 上写了也是无效。
@event.listens_for(engine, "connect")
def _enable_sqlite_fk(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：每次请求一个 db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()