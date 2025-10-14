from fastapi import APIRouter
from .base import router as base_router
from .token import router as token_router

auth_router = APIRouter()
auth_router.include_router(base_router)
auth_router.include_router(token_router)

__all__ = ["auth_router"]
