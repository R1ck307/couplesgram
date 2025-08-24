from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
import json

router = APIRouter(prefix="/couples", tags=["couples"])

def get_couple(db, couple_id: int):
    return db.query(models.Couple).filter(models.Couple.id == couple_id).first()

@router.post("/create")
def create_couple(data: schemas.CoupleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Couple).filter(models.Couple.handle == data.handle).first()
    if existing:
        raise HTTPException(status_code=400, detail="Handle already exists")
    couple = models.Couple(handle=data.handle, display_name=data.display_name, bio=data.bio, members=json.dumps([]))
    db.add(couple)
    db.commit()
    db.refresh(couple)
    return couple

@router.post("/invite")
def invite_partner(invite: schemas.InvitePartner, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == invite.partner_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"couple_id": 1, "message": f"Invite sent to {invite.partner_username}"}

@router.post("/accept")
def accept_invite(accept: schemas.AcceptInvite, db: Session = Depends(get_db)):
    couple = get_couple(db, accept.couple_id)
    if not couple:
        raise HTTPException(status_code=404, detail="Couple not found")
    return {"message": "Invite accepted"}
