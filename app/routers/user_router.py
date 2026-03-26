from fastapi import APIRouter,Depends,HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import schemas
from app.services import user_services
from app.utils.auth import create_access_token, get_current_user

router = APIRouter(prefix=  "/users",tags=["Users"])

@router.post("/register",response_model= schemas.UserResponse)
def register_user(user:schemas.UserCreate,db:Session= Depends(get_db)):
    return user_services.create_user(db,user)


# @router.post('/login')
# def login(user:schemas.UserLogin,db : Session= Depends(get_db)):
#     token = user_services.login_user(db,user)
#     if not token:
#         raise HTTPException(status_code='401',detail="Invalid email or password")
#     return {
#         "access_token":token,
#         "token_type" : "bearer"
#     }
@router.post("/login")
def login_user(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = user_services.login_user(db, form_data)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return current_user