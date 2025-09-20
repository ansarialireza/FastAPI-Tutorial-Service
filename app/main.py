from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

# from fastapi import Body, FastAPI, status, HTTPException
# from typing import Annotated, List
# from schemas import ExpenseCreate, ExpenseUpdate, ExpenseOut
# from datetime import timezone, datetime

# app = FastAPI()

# expenses_temp_db: List[dict] = []


# def unique_id_generator(db):
#     return max([item["id"] for item in db], default=0) + 1


# @app.get(
#     "/expenses",
#     response_model=List[ExpenseOut],
#     status_code=status.HTTP_200_OK,
# )
# async def get_expenses():
#     return expenses_temp_db


# @app.get(
#     "/expenses/{expense_id}",
#     response_model=ExpenseOut,
#     status_code=status.HTTP_200_OK,
# )
# async def get_expense(expense_id: int):
#     expense_in_db = next(
#         (
#             expense
#             for expense in expenses_temp_db
#             if expense["id"] == expense_id
#         ),
#         None,
#     )
#     if expense_in_db is not None:
#         return expense_in_db
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Item with id {expense_id} not found",
#     )


# @app.post(
#     "/expenses",
#     response_model=ExpenseOut,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_expense(item: Annotated[ExpenseCreate, Body()]):
#     item_id = unique_id_generator(expenses_temp_db)
#     expense = {
#         "id": item_id,
#         "description": item.description,
#         "amount": item.amount,
#         "category_id": item.category_id,
#         "created_at": datetime.now(timezone.utc),
#         "updated_at": None,
#     }
#     expenses_temp_db.append(expense)
#     return ExpenseOut(**expense)


# @app.put(
#     "/expenses/{expense_id}",
#     response_model=ExpenseOut,
#     status_code=status.HTTP_200_OK,
# )
# async def update_expense(expense_id: int, item: ExpenseUpdate):
#     expense_in_db = next(
#         (
#             expense
#             for expense in expenses_temp_db
#             if expense["id"] == expense_id
#         ),
#         None,
#     )
#     if expense_in_db is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Item with id {expense_id} not found",
#         )

#     if item.amount is not None:
#         expense_in_db["amount"] = item.amount

#     if item.description is not None:
#         expense_in_db["description"] = item.description
#     expense_in_db["updated_at"] = datetime.now(timezone.utc)
#     return ExpenseOut(**expense_in_db)


# @app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_expense(expense_id: int):
#     expense_in_db = next(
#         (
#             expense
#             for expense in expenses_temp_db
#             if expense["id"] == expense_id
#         ),
#         None,
#     )
#     if expense_in_db is not None:
#         expenses_temp_db.remove(expense_in_db)
#         return
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"Item with id {expense_id} not found",
#     )
