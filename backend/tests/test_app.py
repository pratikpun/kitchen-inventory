"""Integration tests for the kitchen inventory API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app, get_db
from database import Base

TEST_DATABASE_URL = "postgresql://pratikpun@localhost:5432/kitchen_inventory_test"
test_engine = create_engine(TEST_DATABASE_URL)
TestSession = sessionmaker(bind=test_engine)


def override_get_db():
    """Provide a test database session instead of the real one."""
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    """Create all tables before each test."""
    Base.metadata.create_all(bind=test_engine)


def teardown_function():
    """Drop all tables after each test for a clean slate."""
    Base.metadata.drop_all(bind=test_engine)


def test_list_items_empty():
    """Given an empty database, listing items should return an empty list."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    """Given valid item data, creating an item should return it with an id."""
    response = client.post("/items", json={"name": "eggs", "quantity": 12})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "eggs"
    assert data["quantity"] == 12
    assert "id" in data


def test_get_single_item():
    """Given an existing item, fetching it by id should return that item."""
    create_response = client.post("/items", json={"name": "milk", "quantity": 2})
    item_id = create_response.json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "milk"


def test_get_single_item_failure():
    """Given a non-existent id, fetching it should return 404."""
    response = client.get("/items/99")
    assert response.status_code == 404


def test_update_existing_item():
    """Given an existing item, updating it should return the modified item."""
    create_response = client.post("/items", json={"name": "eggs", "quantity": 12})
    item_id = create_response.json()["id"]
    response = client.put(f"/items/{item_id}", json={"name": "eggs", "quantity": 6})
    assert response.status_code == 200
    assert response.json()["quantity"] == 6


def test_delete_item():
    """Given an existing item, deleting it should return 204 and remove it."""
    create_response = client.post("/items", json={"name": "butter", "quantity": 1})
    item_id = create_response.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
