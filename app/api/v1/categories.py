from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud.category import CategoryCRUD
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryOut


router = APIRouter()


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate, db: Session = Depends(get_db)
):
    return CategoryCRUD(db).create(category)


@router.get(
    "/",
    response_model=List[CategoryOut],
    status_code=status.HTTP_200_OK,
)
async def get_(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return CategoryCRUD(db).get_all(skip, limit)


@router.get(
    "/{id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
)
async def get_category(id: int, db: Session = Depends(get_db)):
    db_category = CategoryCRUD(db).get_by_id(id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.put(
    "/{id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
)
async def update_category(
    id: int, category: CategoryUpdate, db: Session = Depends(get_db)
):
    db_category = CategoryCRUD(db).update(id, category)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = CategoryCRUD(db).delete(id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return db_category
