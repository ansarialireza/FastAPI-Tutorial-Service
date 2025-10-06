from multiprocessing import context
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


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh, db: Session = Depends(get_db)
) -> Any:
    token_manager = auth_service.token_manager
    payload = token_manager.verify_token(refresh_data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    username = payload.get("sub")
    user = UserCRUD(db).get_by_username(username)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    access_token = token_manager.create_access_token(
        data={"sub": user.username}
    )
    context = {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_data.refresh_token,
    }
    return context


@router.post("/logout")
async def logout(current_user: Any = Depends(get_current_active_user)) -> Any:
    # Implement Logic for log out , You can delete token or add token to black list
    context = {
        "message": "Succsessfully loged out.",
        "username": current_user.username,
    }
    return context


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    return current_user


@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: Any = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:

    user_crud = UserCRUD(db)

    if not auth_service.authenticate_user(
        db, old_password, current_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="In correct old password",
        )

    is_valid, message = password_manager.validate_password_policy(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=message
        )
    new_hashed_password = password_manager.get_password_hash(new_password)
    user_crud.update_password(current_user.id, new_hashed_password)
    return {"message": "Password changed succsessfully"}


@router.post("/deactive")
async def deactive_account(
    current_user: Any = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    user_crud = UserCRUD(db)
    user_crud.deactivate_user(current_user.id)
    return {"message": "Account deactivated successfully"}


@router.get("/verify")
async def verify_token(
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    # implement verify token logic

    return {
        "message": "Token is valid",
        "user": current_user.username,
        "is_active": current_user.is_active,
    }
