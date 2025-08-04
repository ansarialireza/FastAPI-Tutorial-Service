from fastapi import FastAPI, status, HTTPException, Query
from typing import Annotated
from schemas import ExpenseIn, ExpenseOut

app = FastAPI()


expenses_fake_db = []


def unique_id_generator():
    max_item_id = 0
    expenses_fake_db.sort(key=lambda x: x["item_id"])
    if expenses_fake_db:
        max_item_id = expenses_fake_db[-1]["item_id"]
    return max_item_id + 1


@app.get(
    "/expenses/",
    response_model=list[ExpenseOut],
    status_code=status.HTTP_200_OK,
)
async def get_expenses():
    return expenses_fake_db


@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK,
)
async def get_expense(expense_id: int):
    expense = next(
        (
            expense
            for expense in expenses_fake_db
            if expense["item_id"] == expense_id
        ),
        None,
    )
    if expense is not None:
        return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {expense_id} not found",
    )


@app.post(
    "/expenses/",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(item: Annotated[ExpenseIn, Query()]):
    item_id = unique_id_generator()
    expenses_fake_db.append(
        {
            "item_id": item_id,
            "description": item.description,
            "amount": item.amount
        }
    )
    return {
        "message": "Item created successfully",
        "item_id": item_id,
        "description": item.description,
        "amount": item.amount,
    }


@app.put(
    "/expenses/{expense_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK,
)
async def update_expense(expense_id: int, item: ExpenseIn):
    expense = next(
        (
            expense
            for expense in expenses_fake_db
            if expense["item_id"] == expense_id
        ),
        None,
    )
    if expense is not None:
        expense["description"] = item.description
        expense["amount"] = item.amount
        return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {expense_id} not found",
    )


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(expense_id: int):
    expense = next(
        (
            expense
            for expense in expenses_fake_db
            if expense["item_id"] == expense_id
        ),
        None,
    )
    if expense is not None:
        expenses_fake_db.remove(expense)
        return status.HTTP_204_NO_CONTENT
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {expense_id} not found",
    )
