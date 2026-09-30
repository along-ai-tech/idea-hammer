"""pytest 全局 fixture：内存 SQLite + FastAPI TestClient

策略：每个测试用独立的 in-memory SQLite engine。
TestClient 不触发 main.py 的 lifespan（避免文件 DB 干扰），
直接在 fixture 里 create_all + override get_db。

关键点：SQLAlchemy 默认给 sqlite:///:memory: 装 SingletonThreadPool，
但 pytest 的 fixture teardown 和下一个测试可能在不同线程，导致
create_all 在线程 A 建的表，线程 B 拿 connection 时看到的是另一个
空的 :memory: 数据库（"no such table: posts"）。
解决：poolclass=StaticPool —— 整池只保留一条 connection，跨线程共享
同一个 :memory: 数据库。
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import post, comment, reaction  # noqa: F401  确保 mapper 注册


@pytest.fixture
def db_engine():
    """每个测试一个新 in-memory engine（StaticPool 跨线程共享同一 :memory:）"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # SQLite 默认 PRAGMA foreign_keys=OFF，必须每个 connection 显式开启，
    # 否则 ON DELETE CASCADE 在 DDL 上写了也是无效（与 app/db.py 行为一致）。
    @event.listens_for(engine, "connect")
    def _enable_sqlite_fk(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """in-memory db session"""
    TestingSession = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    session = TestingSession()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    """TestClient（不走 lifespan，依赖 override 直接用 fixture 的 session）"""

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    # 注意：不进 `with TestClient(app)` 是为了避免触发 main.py lifespan
    # （lifespan 用文件 SQLite；test 用 in-memory SQLite；二者独立）
    c = TestClient(app)
    yield c
    app.dependency_overrides.clear()