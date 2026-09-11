from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.db import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)

    # SM-2 间隔重复算法字段
    repetitions = Column(Integer, default=0, nullable=False)
    interval = Column(Integer, default=0, nullable=False)
    easiness_factor = Column(Float, default=2.5, nullable=False)
    due_at = Column(DateTime, nullable=True)
    last_reviewed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
