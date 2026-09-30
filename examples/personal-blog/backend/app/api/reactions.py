"""Reaction API（WI-4）：点赞 / 点踩 + 防重复

端点：
- POST /api/posts/{post_id}/react   EP-7, F-2.7

防重复语义：
- 同 IP + 同 type → 已存在则直接返回 counts（无新行）
- 同 IP + 不同 type → 删旧 + 增新（toggle 语义）
- 不同 IP → 独立计数
- type 仅接受 "up" / "down"，其它值 422
- 博客不存在 → 404

IP 取自 X-Forwarded-For（dev / 反代友好），取不到则用 request.client.host。
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.post import Post
from app.models.reaction import Reaction


router = APIRouter()


# ---------- Schemas ----------

VALID_TYPES = {"up", "down"}


class ReactIn(BaseModel):
    type: str = Field(..., min_length=1, max_length=8)


class ReactOut(BaseModel):
    post_id: int
    up_count: int
    down_count: int
    my_reaction: str  # "up" | "down" | "" (本次响应里本 IP 的最新状态)


# ---------- Helpers ----------

def _client_ip(request: Request) -> str:
    """取 IP：优先 X-Forwarded-For 第一段，否则 request.client.host。"""
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _counts(db: Session, post_id: int) -> tuple[int, int]:
    up = db.query(Reaction).filter(
        Reaction.post_id == post_id, Reaction.type == "up"
    ).count()
    down = db.query(Reaction).filter(
        Reaction.post_id == post_id, Reaction.type == "down"
    ).count()
    return up, down


# ---------- Endpoints ----------

@router.post("/posts/{post_id}/react", response_model=ReactOut)
def react(
    post_id: int,
    payload: ReactIn,
    request: Request,
    db: Session = Depends(get_db),
):
    """F-2.7 点赞 / 点踩"""
    if payload.type not in VALID_TYPES:
        raise HTTPException(status_code=422, detail="type must be 'up' or 'down'")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    ip = _client_ip(request)

    # 1) 该 IP 是否已有 reaction？—— 存在则切 type / 同 type 跳过
    existing = (
        db.query(Reaction)
        .filter(Reaction.post_id == post_id, Reaction.ip == ip)
        .first()
    )

    if existing is None:
        db.add(Reaction(post_id=post_id, ip=ip, type=payload.type))
        my = payload.type
    elif existing.type == payload.type:
        # 同 IP 同 type → no-op
        my = existing.type
    else:
        # 同 IP 切换 type → 删旧增新（toggle 语义）
        db.delete(existing)
        db.flush()
        db.add(Reaction(post_id=post_id, ip=ip, type=payload.type))
        my = payload.type

    try:
        db.commit()
    except IntegrityError:
        # 极端并发：UNIQUE(post_id, ip) 唯一索引冲突 → 回滚，按"已存在"处理
        db.rollback()
        my = (
            db.query(Reaction)
            .filter(Reaction.post_id == post_id, Reaction.ip == ip)
            .first()
            .type
        )

    up, down = _counts(db, post_id)
    return ReactOut(post_id=post_id, up_count=up, down_count=down, my_reaction=my)


@router.get("/posts/{post_id}/reactions", response_model=ReactOut)
def get_reactions(post_id: int, db: Session = Depends(get_db)):
    """顺手：只读计数（前端可单独调用）"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    up, down = _counts(db, post_id)
    return ReactOut(post_id=post_id, up_count=up, down_count=down, my_reaction="")