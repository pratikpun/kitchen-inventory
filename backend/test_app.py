from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app, get_db
from database import Base

# Test database — separate from your real one
TEST_DATABASE_URL = "postgresql://pratikpun@localhost:5432/kitchen_inventory_test"
test_engine = create_engine(TEST_DATABASE_URL)
TestSession = sessionmaker(bind=test_engine)

def override_get_db():
      db = TestSession()
      try:
          yield db
      finally:
          db.close()
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_function():
    Base.metadata.create_all(bind=test_engine)


def teardown_function():
    Base.metadata.drop_all(bind=test_engine)

def test_list_items_empty():
    # Arrange — empty database (teardown wiped it)
    # Act
    response = client.get("/items")
    # Assert
    assert response.status_code == 200
    assert response.json() == []

