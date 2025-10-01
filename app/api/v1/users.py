from fastapi import APIRouter, Depends, status
from app.security.dependencies import get_current_user, get_current_active_user
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.get("/profile", response_model=UserOut, status_code=status.HTTP_200_OK)
async def read_user_profile(current_user=Depends(get_current_active_user)):
    return current_user


@router.put("/me", status_code=status.HTTP_200_OK)
async def update_current_user(
    user: UserUpdate, current_user=Depends(get_current_active_user)
):
    return {"message": "User updated successfully"}
