from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.crud.expense import ExpenseCRUD
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut
from app.security.dependencies import get_current_active_user


router = APIRouter()


@router.post(
    "/",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(
    expense: ExpenseCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return ExpenseCRUD(db).create_expense(expense, current_user.id)


@router.get(
    "/",
    response_model=List[ExpenseOut],
    status_code=status.HTTP_200_OK,
)
def read_expenses(
    category: Optional[str] = None,
    current_user=Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    if category:
        return ExpenseCRUD(db).get_expenses_by_category(
            current_user.id, category, skip, limit
        )
    else:
        return ExpenseCRUD(db).get_user_expenses(current_user.id, skip, limit)


@router.get(
    "/{expense_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK,
)
async def read_expense(
    expense_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_expense = ExpenseCRUD(db).get_user_expense(expense_id, current_user.id)
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
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_expense = ExpenseCRUD(db).update_expense(
        expense_id, current_user.id, expense
    )
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {expense_id} not found",
        )
    return db_expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_expense = ExpenseCRUD(db).delete_expense(expense_id, current_user.id)
    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {expense_id} not found",
        )
    return db_expense
