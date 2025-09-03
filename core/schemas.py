from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    amount: float
    created_at: Optional[date] = date.today()
    description: Optional[str] = None
    category_id: Optional[int] = None
    peyment_method_id: Optional[int] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
