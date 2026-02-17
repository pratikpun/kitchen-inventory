from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from models import Item, ItemCreate, ItemTable


# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items(db: Session = Depends(get_db)) -> list[Item]:
    return db.query(ItemTable).all()


@app.post("/items", status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
    item = ItemTable(**payload.model_dump())           
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    item = db.query(ItemTable).filter(ItemTable.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
    


@app.put("/items/{item_id}")
def get_item(item_id: int, payload: ItemCreate, db: Session = Depends(get_db)) -> Item:
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

    item = db.query(ItemTable).filter(ItemTable.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
