from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.db.session import get_db
from app.security.auth_service import AuthService
from app.security.dependencies import get_current_active_user
from app.schemas.user import UserCreate, UserOut
from app.crud.user import UserCRUD
from app.security.password import password_manager

router = APIRouter()
auth_service = AuthService()


@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_crud = UserCRUD(db)
    db_user = user_crud.get_by_username(user_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {db_user.username} already registered!",
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
            status_code=status.HTTP_400_BAD_REQUEST, detail=message
        )
    hashed_password = password_manager.get_password_hash(
        user_data.hashed_password
    )
    user = user_data.model_copy(update={"hashed_password": hashed_password})
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not password_manager.verify_password(
        form_data.password, db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    tokens = auth_service.generate_tokens(form_data.username)
    return tokens


@router.post("/logout")
async def logout(current_user: Any = Depends(get_current_active_user)) -> Any:
    # TODO: منطق blacklist token رو implement کن
    return {
        "message": "Successfully logged out.",
        "username": current_user.username,
    }
