from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# ---- SQLAlchemy models (database tables) ----


class ItemTable(Base):
    """SQLAlchemy model representing the items table in the database."""

    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)


class RecipeTable(Base):
    """SQLAlchemy model representing the recipes table in the database."""

    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    category = Column(String, nullable=False)

    ingredients = relationship(
        "RecipeIngredientTable", back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredientTable(Base):
    """SQLAlchemy model linking recipes to items with required quantities."""

    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    recipe = relationship("RecipeTable", back_populates="ingredients")
    item = relationship("ItemTable")


# ---- Pydantic models (API request/response schemas) ----


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


class RecipeIngredientCreate(BaseModel):
    """Schema for an ingredient within a recipe creation request."""

    item_id: int
    quantity: int


class RecipeIngredient(BaseModel):
    """Schema for a recipe ingredient response."""

    id: int
    item_id: int
    quantity: int

    class Config:
        from_attributes = True


class RecipeCreate(BaseModel):
    """Schema for creating a new recipe with its ingredients."""

    name: str
    instructions: str
    cooking_time: int
    category: str
    ingredients: list[RecipeIngredientCreate]


class Recipe(BaseModel):
    """Schema for recipe responses. Includes ingredients."""

    id: int
    name: str
    instructions: str
    cooking_time: int
    category: str
    ingredients: list[RecipeIngredient]

    class Config:
        from_attributes = True
