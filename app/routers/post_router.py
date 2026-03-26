from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import schemas
from app.services import post_services
from app.utils.auth import get_current_user
from app.models import models

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=schemas.PostResponse)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):

    return post_services.create_post(db, post, current_user.id)

@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    return post_services.get_posts(db)

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = post_services.get_post(db, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
        post_id: int,
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):

    db_post = post_services.get_post(db, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return post_services.update_post(db, post_id, post)

@router.delete("/{post_id}")
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):

    db_post = post_services.get_post(db, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    post_services.delete_post(db, post_id)

    return {"message": "Post deleted successfully"}