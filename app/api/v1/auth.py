from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from app.db.session import get_db
from app.core.config import Settings
from app.security.auth_service import AuthService
from app.security.dependencies import get_current_user, get_current_active_user
from app.schemas.token import Token, TokenRefresh
from app.schemas.user import UserCreate, UserOut
from app.crud.user import UserCRUD
from app.security.password import PasswordManager

router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()


@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = UserCRUD(db)
    db_user = user.get_by_username(user_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {db_user.username} already registered !",
        )
    db_user = user.get_by_email(user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {db_user.email} already refistred!",
        )

    password_manager = PasswordManager()
    condition, message = password_manager.validate_password_policy(
        user_data.password
    )
    if not condition:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    new_user = user.create(user_data)
    return new_user
