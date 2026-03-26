from sqlalchemy.orm import Session  

from app.models import models
from app.schemas import schemas
from app.utils.hashing import hash_password


def create_user(db:Session,user:schemas.UserCreate):
    hashed_password = hash_password(user.password)

    new_user = models.User(
                    username = user.username,
                    email = user.email,
                    password = hashed_password 
    )   

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

"""
hash_password -	secure password
db.add -	add to DB
db.commit - 	save changes
db.refresh - 	get updated object
"""


#=========================================
#       Create Login Service
#=========================================


from app.utils.hashing import verify_password
from app.utils.auth import create_access_token


def login_user(db, form_data):

    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user:
        return None

    if not verify_password(form_data.password, user.password):
        return None

    return user 


