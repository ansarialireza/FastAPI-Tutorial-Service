from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category as CategoryModel


class CategoryCRUD:

    def __init__(self, db: Session):
        self.db = db

    def create(self, category: CategoryCreate):
        db_category = CategoryModel(**category.model_dump())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get_all(self, skip: int, limit: int):
        return self.db.query(CategoryModel).offset(skip).limit(limit).all()

    def get_by_id(self, id: int):
        return (
            self.db.query(CategoryModel)
            .filter(CategoryModel.id == id)
            .one_or_none()
        )

    def update(self, id: int, category: CategoryUpdate):
        db_category = self.get_by_id(id)
        if db_category is None:
            return None
        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete(self, id: int):
        db_category = self.get_by_id(id)
        if db_category is None:
            return None
        self.db.delete(db_category)
        self.db.commit()
        return db_category
