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
from app.security.password import password_manager

router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()


@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_crud = UserCRUD(db)
    db_user = user_crud.get_by_username(user_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {db_user.username} already registered !",
        )
    db_user = user_crud.get_by_email(user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {db_user.email} already registered!",
        )

    is_valid, message = password_manager.validate_password_policy(
        user_data.hashed_password
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    hashed_password = password_manager.get_password_hash(
        user_data.hashed_password
    )
    user = user_data.model_copy()
    user.hashed_password = hashed_password
    return user_crud.create(user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    user_crud = UserCRUD(db)
    db_user = user_crud.get_by_username(form_data.username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or password is Incorrect",
        )
    password_is_valid = password_manager.verify_password(
        form_data.password, db_user.hashed_password
    )
    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Password is Incorrect",
        )

    tokens = auth_service.generate_tokens(form_data.username)
    return tokens
