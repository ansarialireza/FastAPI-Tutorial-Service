# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from .base import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     expenses = relationship(
#         "Expense", back_populates="user", cascade="all, delete-orphan"
#     )
#     categories = relationship(
#         "Category", back_populates="user", cascade="all, delete-orphan"
#     )

#     def __repr__(self) -> str:
#         return f"<User(username='{self.username}', email='{self.email}')>"
