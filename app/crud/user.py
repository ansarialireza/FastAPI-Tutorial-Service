from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User as UserModel
from typing import List, Optional


class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> UserModel:
        db_user = UserModel(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        return db_user

    def get(self, id: int) -> UserModel | None:
        return (
            self.db.query(UserModel).filter(UserModel.id == id).one_or_none()
        )

    def get_by_email(self, email: str) -> UserModel | None:
        return (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .one_or_none()
        )

    def get_by_username(self, username: str) -> UserModel | None:
        return (
            self.db.query(UserModel)
            .filter(UserModel.username == username)
            .one_or_none()
        )

    def get_all(self, skip: int, limit: int) -> List[UserModel]:
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def get_active_users(
        self, skip: int = 0, limit: int = 100
    ) -> List[UserModel]:
        return (
            self.db.query(UserModel)
            .filter(UserModel.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def deactivate_user(self, id: int) -> Optional[UserModel]:
        db_user = self.get(id)
        if db_user is None:
            return None
        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def active_user(self, id: int) -> Optional[UserModel]:
        db_user = self.get(id)
        if db_user is None:
            return None
        if not (bool(db_user.is_active)):
            db_user.is_active = True
            self.db.commit()
            self.db.refresh(db_user)
            return db_user

        return db_user

    def update(self, id: int, user: UserUpdate):
        db_user = self.get(id)
        if db_user is None:
            return None
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, id: int):
        db_user = self.get(id)
        if db_user is None:
            return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user
