from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def create_post(db:Session ,post:schemas.PostCreate,user_id:int):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        user_id=user_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
        
    return new_post

def get_posts(db:Session):
    return db.query(models.Post).all()

def get_post(db:Session,post_id : int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()



def update_post(db: Session, post_id: int, post_data: schemas.PostCreate):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        return None

    post.title = post_data.title
    post.content = post_data.content
    post.published = post_data.published

    db.commit()
    db.refresh(post)

    return post

def delete_post(db: Session, post_id: int):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        return None

    db.delete(post)
    db.commit()

    return post