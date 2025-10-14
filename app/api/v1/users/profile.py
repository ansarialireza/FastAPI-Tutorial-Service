from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app.db.session import get_db
from app.security.auth_service import AuthService
from app.security.dependencies import get_current_user, get_current_active_user
from app.schemas.user import UserOut, UserUpdate
from app.crud.user import UserCRUD
from app.security.password import password_manager

router = APIRouter()
auth_service = AuthService()


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user_profile(current_user=Depends(get_current_active_user)):
    return current_user


@router.put("/me", status_code=status.HTTP_200_OK)
async def update_current_user(
    user: UserUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # TODO: منطق کامل آپدیت (مثل user_crud.update)
    user_crud = UserCRUD(db)
    updated_user = user_crud.update(
        current_user.id, user
    )  # فرض بر وجود متد update
    return {"message": "User updated successfully", "user": updated_user}


@router.post("/password")
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
            detail="Incorrect old password",
        )
    is_valid, message = password_manager.validate_password_policy(new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=message
        )
    new_hashed_password = password_manager.get_password_hash(new_password)
    user_crud.update_password(current_user.id, new_hashed_password)
    return {"message": "Password changed successfully"}


@router.post("/deactivate")
async def deactivate_account(
    current_user: Any = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    user_crud = UserCRUD(db)
    user_crud.deactivate_user(current_user.id)
    return {"message": "Account deactivated successfully"}


@router.patch("/activate")
async def activate_account(
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_crud = UserCRUD(db)
    user_crud.activate_user(current_user.id)
    return {"message": "Account activated successfully"}


@router.delete("/user")
async def delete_account(
    current_user: Any = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_crud = UserCRUD(db)
    user_crud.delete_user(current_user.id)
    return {"message": "Account deleted successfully"}
