from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------------------------
# Category Schemas
# -------------------------
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class CategoryOut(CategoryBase):
    id: int

    model_config = {"from_attributes": True}


# -------------------------
# Expense Schemas
# -------------------------
class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=200)


class ExpenseCreate(ExpenseBase):
    category_id: int


class ExpenseUpdate(ExpenseBase):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=200)
    category_id: Optional[int] = None


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_id: int

    model_config = {"from_attributes": True}
