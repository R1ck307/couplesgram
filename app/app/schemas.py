from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    date_of_birth: str

class CoupleCreate(BaseModel):
    handle: str
    display_name: str
    bio: Optional[str] = ""

class InvitePartner(BaseModel):
    partner_username: str

class AcceptInvite(BaseModel):
    couple_id: int

class PostCreate(BaseModel):
    caption: Optional[str] = None

class MessageCreate(BaseModel):
    to_couple_id: int
    body: str
