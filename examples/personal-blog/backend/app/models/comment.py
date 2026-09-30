"""Comment ORM 模型（WI-3）"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nickname = Column(String(50), nullable=False)
    content = Column(String(2000), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    post = relationship("Post", back_populates="comments")


# 复合索引：按博客拉评论列表时按时间排序（plan §5）
Index("idx_comments_post_created", Comment.post_id, Comment.created_at.desc())