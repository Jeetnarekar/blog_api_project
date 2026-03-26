from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time



#create user schema
class UserCreate(BaseModel):
    username : str
    email : str
    password : str


class UserLogin(BaseModel):
    email : str
    password : str

"""
    This is used when sending user data to the client.
    Important: password is not included
"""
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    """
        Enable ORM Mode
        FastAPI needs ORM mode to convert SQLAlchemy models → Pydantic schemas.
        Add this inside response schemas.
        (This replaces the older orm_mode=True in new Pydantic versions.)
    """
    class Config:
        from_attributes = True




class PostCreate(BaseModel):
    title : str
    content : str
    published : bool = True


class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool = True
    created_at: Optional[datetime] 
    user_id  : int

    class config:
        from_attributes = True
