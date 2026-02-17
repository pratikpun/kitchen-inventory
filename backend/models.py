from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

# SQLAlchemy model validation
class ItemTable(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)



class ItemCreate(BaseModel):
    name: str
    quantity: int


class Item(BaseModel):
    id: int
    name: str
    quantity: int

    class Config:
        from_attributes = True
