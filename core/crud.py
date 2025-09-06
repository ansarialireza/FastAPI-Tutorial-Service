import re
from sqlalchemy.orm import Session
from core import models, schemas


class ExpenseCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, expense: schemas.ExpenseCreate):
        db_expense = models.Expense(**expense.model_dump())
        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(models.Expense).offset(skip).limit(limit).all()

    def get_by_id(self, id: int):
        return (
            self.db.query(models.Expense)
            .filter(models.Expense.id == id)
            .first()
        )

    def update(self, id: int, expense: schemas.ExpenseUpdate):
        db_expense = self.get_by_id(id)
        if not db_expense:
            return None
        for key, value in expense.model_dump(exclude_unset=True).items():
            setattr(db_expense, key, value)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense

    def delete(self, id: int):
        db_expense = self.get_by_id(id)
        if not db_expense:
            return None
        self.db.delete(db_expense)
        self.db.commit()
        return db_expense
