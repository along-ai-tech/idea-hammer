"""Reaction ORM 模型（WI-4）

点赞 / 点踩 = 一行 (post_id, ip, type)，UNIQUE(post_id, ip) 防重复。
同 IP 切换 type（up → down）= delete 旧 + insert 新，或 UPSERT。
v0 简化：API 用 "toggle 语义"，不存在则新增、存在则删除（同 IP 不留痕）。
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db import Base


class Reaction(Base):
    __tablename__ = "reactions"
    __table_args__ = (
        UniqueConstraint("post_id", "ip", name="uniq_post_ip"),
    )

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