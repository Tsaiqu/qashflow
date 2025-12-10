import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db():
    # Setup: create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: remove the database file
    os.remove("./test.db")


def test_create_transaction():
    response = client.post(
        "/transactions/",
        json={
            "name": "Test Transaction",
            "category": "Testing",
            "amount": 100.0,
            "date": "2023-01-01",
            "transaction_type": "expense",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Transaction"
    assert data["category"] == "Testing"
    assert data["amount"] == 100.0
    assert "id" in data


def test_list_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_summary():
    client.post(
        "/transactions/",
        json={
            "name": "Income",
            "category": "Salary",
            "amount": 500.0,
            "date": "2023-01-02",
            "transaction_type": "income",
        },
    )
    client.post(
        "/transactions/",
        json={
            "name": "Expense",
            "category": "Groceries",
            "amount": 50.0,
            "date": "2023-01-03",
            "transaction_type": "expense",
        },
    )
    response = client.get("/summary/")
    assert response.status_code == 200
    data = response.json()
    assert "total_income" in data
    assert "total_expenses" in data


def test_predict_category_model_not_found(monkeypatch):
    # Mock the predict_category function to simulate the model not being available
    monkeypatch.setattr("main.predict_category", lambda name: None)
    response = client.get("/predict_category?name=some_transaction")
    assert response.status_code == 404
    assert response.json() == {"detail": "Model not trained yet. Please train the model first."}