from fastapi import FastAPI, status, HTTPException
from typing import Annotated
from pydantic import BaseModel
import random
import uuid

app = FastAPI()


expenses_fake_db = []


class ExpenseMsneger(BaseModel):
    description: str
    amount: float


@app.get("/expenses/", status_code=status.HTTP_200_OK, tags=["get"])
async def get_expenses():
    return expenses_fake_db


@app.get("/expenses/{expense_id}", status_code=status.HTTP_200_OK, tags=["get"])
async def get_expense(expense_id: int):
    for expense in expenses_fake_db:
        if expense["item_id"] == expense_id:
            return expense
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {expense_id} not found")


@app.post("/expenses/", status_code=status.HTTP_201_CREATED)
async def create_expense(description: str, amount: float):
    item_id = uuid.uuid4()
    expenses_fake_db.append(
        {"item_id": item_id, "description": description, "amount": amount}
    )
    return {
        "message": "Item created successfully",
        "id": item_id,
        "description": description,
        "amount": amount,
    }


@app.put("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
async def update_expense(expense_id: int, description: str, amount: float):
    for expense in expenses_fake_db:
        if expense["item_id"] == expense_id:
            expense["description"] = description
            expense["amount"] = amount
        return expense
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {expense_id} not found")


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
async def delete_expense(expense_id: int):
    for expense in expenses_fake_db:
        if expense["item_id"] == expense_id:
            expenses_fake_db.remove(expense)
            return status.HTTP_204_NO_CONTENT
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with id {expense_id} not found")
