from fastapi import FastAPI
from app.api.v1 import (
    categories_router,
    expenses_router,
    auth_router,
    users_router,
)
from app.core.config import settings
from app.db.session import engine
from app.db import base


def create_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
    app.include_router(
        expenses_router, prefix="/api/v1/expenses", tags=["expenses"]
    )
    app.include_router(
        categories_router, prefix="/api/v1/categories", tags=["categories"]
    )

    return app


app = create_application()
