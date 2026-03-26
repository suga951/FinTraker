import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

from app.main import app
from app.api.deps import get_db
from app.database import Base
from app.core.config import settings

# Test database setup (using the same DB but we could use a test one)
# For this environment, we'll just use the existing one or a mock if available.
# Since the environment has a living Postgres, we'll just use it.

client = TestClient(app)

def get_auth_header(email="test@example.com", password="password123"):
    # Registration
    client.post("/auth/register", json={"email": email, "password": password})
    # Login
    response = client.post("/auth/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_category():
    headers = get_auth_header("cat_test@example.com")
    response = client.post(
        "/categories/",
        json={"name": "Food", "type": "expense"},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Food"

def test_create_transaction():
    headers = get_auth_header("tx_test@example.com")
    # First create a category
    cat_resp = client.post(
        "/categories/",
        json={"name": "Salary", "type": "income"},
        headers=headers
    )
    cat_id = cat_resp.json()["id"]
    
    # Create transaction
    response = client.post(
        "/transactions/",
        json={
            "description": "Monthly Salary",
            "amount": "5000.00",
            "type": "income",
            "category_id": cat_id
        },
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Monthly Salary"
    assert Decimal(response.json()["amount"]) == Decimal("5000.00")

def test_get_transactions():
    headers = get_auth_header("list_test@example.com")
    client.post("/categories/", json={"name": "Rent", "type": "expense"}, headers=headers)
    cat_id = client.get("/categories/", headers=headers).json()[0]["id"]
    
    client.post(
        "/transactions/",
        json={
            "description": "Rent March",
            "amount": "1200.00",
            "type": "expense",
            "category_id": cat_id
        },
        headers=headers
    )
    
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
