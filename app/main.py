from fastapi import FastAPI
from app.database import engine
from app.models import models
from app.routers import user_router
from app.routers import post_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(user_router.router)
app.include_router(post_router.router)