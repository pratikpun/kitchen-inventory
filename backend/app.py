"""Kitchen inventory API with CRUD endpoints for managing items."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Item, ItemCreate, ItemTable

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
