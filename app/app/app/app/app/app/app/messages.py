from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/send")
def send_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    message = models.Message(from_couple_id=1, to_couple_id=msg.to_couple_id, body=msg.body)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/thread/{other_couple_id}")
def get_thread(other_couple_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(
        ((models.Message.from_couple_id==1) & (models.Message.to_couple_id==other_couple_id)) |
        ((models.Message.from_couple_id==other_couple_id) & (models.Message.to_couple_id==1))
    ).order_by(models.Message.created_at).all()
    return messages
