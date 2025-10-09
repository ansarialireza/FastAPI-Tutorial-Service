from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(200), nullable=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_category"),
    )

    def __repr__(self):
        return f"<Category(name='{self.name}, user_id={self.user_id})>"
