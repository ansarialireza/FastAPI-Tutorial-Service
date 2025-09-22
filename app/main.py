from fastapi import FastAPI
from app import models
from app.database import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.expenses import router as expenses_router
from app.api.v1.categories import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
