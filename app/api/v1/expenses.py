from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud.expense import ExpenseCRUD
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut

router = APIRouter()


@router.post(
    "/",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(
    expense: ExpenseCreate, db: Session = Depends(get_db)
):
    return ExpenseCRUD(db).create(expense)


@router.get(
    "/",
    response_model=List[ExpenseOut],
    status_code=status.HTTP_200_OK,
)
def get_(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return ExpenseCRUD(db).get_all(skip, limit)


@router.get(
    "/{expense_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK,
)
async def get_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = ExpenseCRUD(db).get_by_id(expense_id)
    if db_expense is not None:
        return db_expense
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {expense_id} not found",
        )


@router.put(
    "/{expense_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK,
)
async def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
):
    db_expense = ExpenseCRUD(db).update(expense_id, expense)
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {expense_id} not found",
        )
    return db_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = ExpenseCRUD(db).delete(expense_id)
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {expense_id} not found",
        )
    return db_expense
