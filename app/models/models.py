from sqlalchemy import String,Column,Integer,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime   
from app.database import Base



class User(Base):
    __tablename__ = "users"

    id =  Column(Integer,primary_key=True)
    username = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    posts = relationship("Post",back_populates="owner")
    #User.posts → gives all posts created by that user

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User",back_populates = "posts")
    #Post.owner → gives the user who created the post


