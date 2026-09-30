"""Comment API（WI-3）：创建评论 + 删除评论

端点：
- POST   /api/posts/{post_id}/comments   EP-6, F-2.6 创建评论
- DELETE /api/comments/{comment_id}      EP-9, F-2.9 删除评论

依赖：app.models.comment 必须先 import 才能让 Base 知道表。
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.post import Post
from app.models.comment import Comment

# 显式 import —— 确保 ORM 类被注册到 Base.metadata
from app.models import comment as _comment  # noqa: F401


router = APIRouter()


# ---------- Schemas ----------

class CommentCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=2000)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    nickname: str
    content: str
    created_at: str


def _to_out(c: Comment) -> CommentOut:
    return CommentOut(
        id=c.id,
        post_id=c.post_id,
        nickname=c.nickname,
        content=c.content,
        created_at=c.created_at.isoformat() if c.created_at else "",
    )


# ---------- Endpoints ----------

@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(post_id: int, payload: CommentCreate, db: Session = Depends(get_db)):
    """F-2.6 给博客写评论"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = Comment(
        post_id=post_id,
        nickname=payload.nickname,
        content=payload.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return _to_out(comment)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """F-2.9 删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    # 清 identity map，确保同一 session 内下次按 id 查时不会拿到已删的"幽灵"对象
    db.expire_all()
    return None