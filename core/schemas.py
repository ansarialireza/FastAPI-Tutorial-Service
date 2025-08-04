from pydantic import BaseModel, Field
from datetime import datetime


class ExpenseIn(BaseModel):
    description: str = Field(
        max_length=255,
        min_length=1,
        description="Description of the expense, must be between 1 and 255",
    )
    amount: float = Field(
        ...,
        gt=0,
        description="The amount must be greater than zero")


class ExpenseOut(ExpenseIn):
    item_id: int
    access_date: datetime = Field(
        default_factory=datetime.now,
        description="Date of time accsess to expense"
    )
