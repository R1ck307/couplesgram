from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_of_birth = Column(String)

class Couple(Base):
    __tablename__ = "couples"
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String, unique=True)
    display_name = Column(String)
    bio = Column(Text)
    members = Column(Text)  # JSON list of user ids

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    couple_id = Column(Integer, ForeignKey("couples.id"))
    type = Column(String)  # "image" or "video"
    file_path = Column(String)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    from_couple_id = Column(Integer, ForeignKey("couples.id"))
    to_couple_id = Column(Integer, ForeignKey("couples.id"))
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
