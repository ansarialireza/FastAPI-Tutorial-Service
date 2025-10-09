from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category as CategoryModel


class CategoryCRUD:

    def __init__(self, db: Session):
        self.db = db

    def create_category(
        self, user_id, category: CategoryCreate
    ) -> CategoryModel:
        db_category = CategoryModel(**category.model_dump(), user_id=user_id)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get_user_category(
        self, category_id: int, user_id: int
    ) -> Optional[CategoryModel]:
        return (
            self.db.query(CategoryModel)
            .filter(
                CategoryModel.id == category_id,
                CategoryModel.user_id == user_id,
            )
            .one_or_none()
        )

    def get_user_categories(
        self, user_id: int, skip: int, limit: int
    ) -> List[CategoryModel]:
        return (
            self.db.query(CategoryModel)
            .filter(CategoryModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_category(
        self, category_id: int, user_id: int, category: CategoryUpdate
    ) -> Optional[CategoryModel]:
        db_category = self.get_user_category(
            category_id=category_id, user_id=user_id
        )
        if db_category is None:
            return None
        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete_category(self, category_id: int, user_id: int):
        db_category = self.get_user_category(
            category_id=category_id, user_id=user_id
        )
        if db_category is None:
            return None
        self.db.delete(db_category)
        self.db.commit()
        return db_category
