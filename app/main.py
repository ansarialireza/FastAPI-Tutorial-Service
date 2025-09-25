from fastapi import FastAPI
from app.api.v1 import auth, categories, expenses
from app.core.config import settings
from app.db.session import engine
from app.db import base


def create_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(
        expenses.router, prefix="/api/v1/expenses", tags=["expense"]
    )
    app.include_router(
        categories.router, prefix="/api/v1/categories", tags=["categories"]
    )

    return app


app = create_application()
