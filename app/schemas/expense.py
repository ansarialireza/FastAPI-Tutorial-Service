from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=200)
    currency: Optional[str] = Field("USD", min_length=3, max_length=3)
    model_config = ConfigDict(from_attributes=True)


class ExpenseCreate(ExpenseBase):
    category_id: int


class ExpenseUpdate(ExpenseBase):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=200)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    category_id: Optional[int] = None


class ExpenseOut(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_id: int
