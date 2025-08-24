from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, moderation
from .database import get_db
import os, shutil
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
def create_post(file: UploadFile = File(...), caption: str = Form(None), db: Session = Depends(get_db)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["jpg","jpeg","png","webp","mp4","mov","m4v","webm"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    filepath = os.path.join(UPLOAD_DIR, f"{datetime.utcnow().timestamp()}_{file.filename}")
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    if caption and not moderation.text_is_safe(caption):
        raise HTTPException(status_code=400, detail="Caption not allowed")
    if not moderation.file_is_safe(filepath):
        raise HTTPException(status_code=400, detail="File not allowed")
    post = models.Post(couple_id=1, type="image" if ext in ["jpg","jpeg","png","webp"] else "video", file_path=filepath, caption=caption)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get("/feed")
def get_feed(db: Session = Depends(get_db)):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()

@router.get("/media/{post_id}")
def get_media(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post or not os.path.exists(post.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return {"file_path": post.file_path}
