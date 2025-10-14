from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app.db.session import get_db
from app.security.auth_service import AuthService
from app.security.dependencies import get_current_active_user
from app.schemas.token import Token, TokenRefresh
from app.crud.user import UserCRUD

router = APIRouter()
auth_service = AuthService()


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
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_data.refresh_token,
    }


@router.get("/verify")
async def verify_token(
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    # TODO: منطق verify کامل (مثل چک blacklist)
    return {
        "message": "Token is valid",
        "user": current_user.username,
        "is_active": current_user.is_active,
    }
