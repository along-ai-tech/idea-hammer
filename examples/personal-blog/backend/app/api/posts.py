"""Post API：CRUD + 置顶（WI-2，5 个端点 + PATCH pin = 实际 6 端点）

端点：
- POST   /api/posts                  F-2.1 创建
- GET    /api/posts                  F-2.2 列表（分页 + 置顶优先）
- GET    /api/posts/{id_or_slug}     F-2.3 详情（WI-5：含 comments + counts）
- PUT    /api/posts/{id}             F-2.4 编辑
- DELETE /api/posts/{id}             F-2.5 删除
- PATCH  /api/posts/{id}/pin         F-2.8 置顶切换
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models.post import Post
from app.models.comment import Comment
from app.models.reaction import Reaction
from app.api.reactions import _counts  # 复用计数 helper（避免重复 query）

# 显式 import —— 确保 mapper 注册到 Base.metadata
from app.models import comment as _comment  # noqa: F401
from app.models import reaction as _reaction  # noqa: F401


router = APIRouter()


# ---------- Pydantic Schemas ----------

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    is_pinned: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class CommentOut(BaseModel):
    """详情内嵌的评论（与 app/api/comments.py 同构；内联是因为详情聚合要它）"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    nickname: str
    content: str
    created_at: str


class PostOut(BaseModel):
    """列表用（不聚合）。"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: str
    is_pinned: bool
    created_at: str  # ISO 字符串
    updated_at: str


class PostDetailOut(PostOut):
    """详情用（聚合：评论 + 计数）。"""
    comments: List[CommentOut] = []
    up_count: int = 0
    down_count: int = 0


# ---------- Helpers ----------

def _generate_slug(title: str, db: Session) -> str:
    """slug 默认 = title；冲突追加 -id 后缀。"""
    base = title.strip()
    candidate = base
    suffix = 0
    while db.query(Post).filter(Post.slug == candidate).first() is not None:
        suffix += 1
        candidate = f"{base}-{suffix}"
    return candidate


def _to_out(post: Post) -> PostOut:
    return PostOut(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        is_pinned=post.is_pinned,
        created_at=post.created_at.isoformat() if post.created_at else "",
        updated_at=post.updated_at.isoformat() if post.updated_at else "",
    )


def _to_detail(post: Post, db: Session) -> PostDetailOut:
    """详情聚合：comments（按 created_at 升序）+ up/down 计数。

    selectinload 避免 N+1（一次 extra SELECT 而非按每条评论一条）。
    """
    comments_sorted = sorted(post.comments, key=lambda c: c.created_at)
    up, down = _counts(db, post.id)
    return PostDetailOut(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        is_pinned=post.is_pinned,
        created_at=post.created_at.isoformat() if post.created_at else "",
        updated_at=post.updated_at.isoformat() if post.updated_at else "",
        comments=[
            CommentOut(
                id=c.id,
                post_id=c.post_id,
                nickname=c.nickname,
                content=c.content,
                created_at=c.created_at.isoformat() if c.created_at else "",
            )
            for c in comments_sorted
        ],
        up_count=up,
        down_count=down,
    )


def _get_post_or_404(db: Session, id_or_slug: str) -> Post:
    """按 id（int） 或 slug（str）查；不存在 → 404。详情端点用 selectinload 拉评论"""
    q = db.query(Post).options(selectinload(Post.comments))
    post = None
    if id_or_slug.isdigit():
        post = q.filter(Post.id == int(id_or_slug)).first()
    if post is None:
        post = q.filter(Post.slug == id_or_slug).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# ---------- Endpoints ----------

@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    """F-2.1 创建博客"""
    post = Post(
        title=payload.title,
        slug=_generate_slug(payload.title, db),
        content=payload.content,
        is_pinned=payload.is_pinned,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return _to_out(post)


@router.get("/posts", response_model=List[PostOut])
def list_posts(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """F-2.2 列表：置顶优先（按 is_pinned DESC, created_at DESC），分页"""
    posts = (
        db.query(Post)
        .order_by(Post.is_pinned.desc(), Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [_to_out(p) for p in posts]


@router.get("/posts/{id_or_slug}", response_model=PostDetailOut)
def get_post(id_or_slug: str, db: Session = Depends(get_db)):
    """F-2.3 详情（按 id 或 slug；含评论列表 + up/down 计数）"""
    return _to_detail(_get_post_or_404(db, id_or_slug), db)


@router.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    """F-2.4 编辑"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = payload.title
    post.content = payload.content
    post.is_pinned = payload.is_pinned
    post.slug = _generate_slug(payload.title, db)
    db.commit()
    db.refresh(post)
    return _to_out(post)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """F-2.5 删除"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None


@router.patch("/posts/{post_id}/pin", response_model=PostOut)
def toggle_pin(post_id: int, db: Session = Depends(get_db)):
    """F-2.8 切换置顶"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.is_pinned = not post.is_pinned
    db.commit()
    db.refresh(post)
    return _to_out(post)