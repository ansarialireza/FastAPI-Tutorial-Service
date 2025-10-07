from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from app.models.expense import Expense as ExpenseModel
from app.models.category import Category as CategoryModel


class ExpenseCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(
        self, expense: ExpenseCreate, user_id: int
    ) -> ExpenseModel:
        db_expense = ExpenseModel(**expense.model_dump(), user_id=user_id)
        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense

    def get_user_expense(
        self, expense_id: int, user_id: int
    ) -> Optional[ExpenseModel]:
        return (
            self.db.query(ExpenseModel)
            .filter(
                ExpenseModel.id == expense_id, ExpenseModel.user_id == user_id
            )
            .one_or_none()
        )

    def get_user_expenses(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> List[ExpenseModel]:
        return (
            self.db.query(ExpenseModel)
            .filter(ExpenseModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_expenses_by_category(
        self,
        user_id: int,
        category: str,
        skip: int = 0,
        limit: int = 10,
    ) -> List[ExpenseModel]:
        return (
            self.db.query(ExpenseModel)
            .filter(
                ExpenseModel.user_id == user_id,
                ExpenseModel.category == category,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_expense(
        self, expense_id: int, user_id: int, expense: ExpenseUpdate
    ) -> Optional[ExpenseModel]:
        db_expense = self.get_user_expense(
            expense_id=expense_id, user_id=user_id
        )
        if db_expense is None:
            return None
        for key, value in expense.model_dump(exclude_unset=True).items():
            setattr(db_expense, key, value)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense

    def delete_expense(
        self, expense_id: int, user_id: int
    ) -> ExpenseModel | None:
        db_expense = self.get_user_expense(
            expense_id=expense_id, user_id=user_id
        )
        if not db_expense:
            return None
        self.db.delete(db_expense)
        self.db.commit()
        return db_expense
