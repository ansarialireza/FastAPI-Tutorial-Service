from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.db.session import get_db
from app.crud.user import UserCRUD

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserCRUD(db).create(user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user} not found",
        )
    return db_user


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return UserCRUD(db).get_all(skip, limit)


@router.get("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db)):
    db_user = UserCRUD(db).get(id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} not found",
        )
    return db_user


@router.put("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(
    id: int, user: UserUpdate, db: Session = Depends(get_db)
):
    db_user = UserCRUD(db).update(id, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} not found",
        )
    return db_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = UserCRUD(db).delete(id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} not found",
        )
    return db_user
