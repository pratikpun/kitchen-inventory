"""Kitchen inventory API with CRUD endpoints for managing items."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import (
    Item,
    ItemCreate,
    ItemTable,
    Recipe,
    RecipeCreate,
    RecipeIngredientTable,
    RecipeTable,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Provide a database session for a single request, then close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple status check to verify the API is running."""
    return {"status": "ok"}


@app.get("/items")
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    """Return all items in the inventory."""
    return db.query(ItemTable).all()


@app.post("/items", status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
    """Add a new item to the inventory and return it with a generated id."""
    item = ItemTable(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """Return a single item by its id. Raises 404 if not found."""
    item = db.query(ItemTable).filter(ItemTable.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
    """Update an existing item by its id. Raises 404 if not found."""
    item = db.query(ItemTable).filter(ItemTable.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = payload.name
    item.quantity = payload.quantity
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an item by its id. Raises 404 if not found."""
    item = db.query(ItemTable).filter(ItemTable.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()


@app.post("/recipes", status_code=201)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)) -> Recipe:
    """
    Create a new recipe, Add the recipe without ingredients
    then loops the ingredients to add to the database.
    """
    recipe = RecipeTable(**payload.model_dump(exclude={"ingredients"}))
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    for i in payload.ingredients:
        recipe_ingredients = RecipeIngredientTable(
            recipe_id=recipe.id, item_id=i.item_id, quantity=i.quantity
        )
        db.add(recipe_ingredients)
    db.commit()

    db.refresh(recipe)

    return recipe


@app.get("/recipes")
def get_all_recipes(db: Session = Depends(get_db)) -> list[Recipe]:
    """Return all items in the Recipe table."""
    return db.query(RecipeTable).all()


# @app.get("/recipes/available")
# def get_available_recipes(db:Session = Depends(get_db)) -> list[Recipe]:
#     all_recipes =  db.query(RecipeTable).all()
#     result = []
#     for recipe in all_recipes:
#         for ingredients in recipe['ingredients']:


# return all_recipes
@app.get("/recipes/{recipe_id}")
def get_one_recipe(recipe_id: int, db: Session = Depends(get_db)) -> Recipe:
    """Return one item in the Recipe table."""
    recipe = db.query(RecipeTable).filter(RecipeTable.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a recipe by its id. Raises 404 if not found."""
    recipe = db.query(RecipeTable).filter(RecipeTable.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
