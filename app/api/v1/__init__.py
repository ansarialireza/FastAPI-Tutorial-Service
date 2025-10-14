# export مستقیم routerها برای import در main.py
from .auth import auth_router
from .users import users_router
from .expenses import router as expenses_router
from .categories import router as categories_router

__all__ = [
    "auth_router",
    "users_router",
    "expenses_router",
    "categories_router",
]
