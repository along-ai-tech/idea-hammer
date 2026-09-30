"""Reaction ORM 模型（WI-4 stub，WI-3 先声明避免 Post mapper 失败）

点赞 / 点踩 = 一行 (post_id, ip, type)，用 UNIQUE(post_id, ip) 防重复。
WI-4 会接入 API。
"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ip = Column(String(64), nullable=False)
    type = Column(String(8), nullable=False)  # "up" | "down"
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="reactions")