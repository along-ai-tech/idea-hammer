from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.card import Card
from app.services.spaced_repetition import calculate_next_review

router = APIRouter()


class CardStudyOut(BaseModel):
    """复习用的卡片 schema，含 SM-2 调度字段"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    front: str
    back: str
    repetitions: int
    interval: int
    easiness_factor: float
    due_at: Optional[datetime] = None
    last_reviewed_at: Optional[datetime] = None


class ReviewRequest(BaseModel):
    """复习请求：quality 0-5（< 3 答错，>= 3 答对）"""
    quality: int = Field(ge=0, le=5)


class StudyStats(BaseModel):
    """学习统计"""
    due_now: int
    total: int
    learned: int


@router.get("/study/queue", response_model=List[CardStudyOut])
def get_study_queue(db: Session = Depends(get_db), limit: int = 20):
    """获取当前待复习的卡片队列（due_at <= now 或从未复习过）"""
    now = datetime.utcnow()
    cards = (
        db.query(Card)
        .filter(or_(Card.due_at.is_(None), Card.due_at <= now))
        .order_by(Card.due_at.asc().nulls_first())
        .limit(limit)
        .all()
    )
    return cards


@router.post("/study/{card_id}/review", response_model=CardStudyOut)
def review_card(card_id: int, payload: ReviewRequest, db: Session = Depends(get_db)):
    """提交一次复习结果，按 SM-2 算法更新卡片调度状态"""
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    updated = calculate_next_review(card, payload.quality)
    card.repetitions = updated.repetitions
    card.interval = updated.interval
    card.easiness_factor = updated.easiness_factor
    card.due_at = updated.due_at
    card.last_reviewed_at = updated.last_reviewed_at
    db.commit()
    db.refresh(card)
    return card


@router.get("/study/stats", response_model=StudyStats)
def get_study_stats(db: Session = Depends(get_db)):
    """学习统计：当前待复习数 / 总卡片数 / 已学过数"""
    now = datetime.utcnow()
    total = db.query(Card).count()
    due_now = db.query(Card).filter(
        or_(Card.due_at.is_(None), Card.due_at <= now)
    ).count()
    learned = db.query(Card).filter(Card.repetitions > 0).count()
    return StudyStats(due_now=due_now, total=total, learned=learned)
