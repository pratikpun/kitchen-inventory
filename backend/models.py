from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import Base


class ItemTable(Base):
    """SQLAlchemy model representing the items table in the database."""

    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)


class ItemCreate(BaseModel):
    """Schema for creating a new item. Used to validate POST and PUT request bodies."""

    name: str
    quantity: int


class Item(BaseModel):
    """Schema for item responses. Includes the database-generated id."""

    id: int
    name: str
    quantity: int

    class Config:
        from_attributes = True
