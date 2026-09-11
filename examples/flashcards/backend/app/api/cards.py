from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.card import Card

router = APIRouter()


class CardCreate(BaseModel):
    front: str
    back: str


class CardUpdate(BaseModel):
    front: str
    back: str


class CardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    front: str
    back: str


@router.post("/cards", response_model=CardOut, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate, db: Session = Depends(get_db)):
    card = Card(front=payload.front, back=payload.back)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.get("/cards", response_model=List[CardOut])
def list_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()


@router.get("/cards/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/cards/{card_id}", response_model=CardOut)
def update_card(card_id: int, payload: CardUpdate, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card.front = payload.front
    card.back = payload.back
    db.commit()
    db.refresh(card)
    return card


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return None
