from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
    Index,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=func.now())
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    __table_args__ = (
        Index("ix_expenses_category_created", "category_id", "created_at"),
    )

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, amount={self.amount}, "
            f"date={self.created_at})>"
        )
