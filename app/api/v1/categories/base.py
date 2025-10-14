from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud.category import CategoryCRUD
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.security.dependencies import get_current_active_user


router = APIRouter()


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return CategoryCRUD(db).create_category(category, current_user.id)


@router.get(
    "/",
    response_model=List[CategoryOut],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    current_user=Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return CategoryCRUD(db).get_user_categories(current_user.id, skip, limit)


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
)
async def get_category(
    category_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_category = CategoryCRUD(db).get_user_category(
        category_id, current_user.id
    )
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.put(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_category = CategoryCRUD(db).update_category(
        category_id, current_user.id, category
    )
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_category = CategoryCRUD(db).delete_category(
        category_id, current_user.id
    )
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category
