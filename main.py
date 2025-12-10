from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import models
import schemas
from database import SessionLocal, engine
import joblib
from ml.predict import predict_category, load_model

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Load the machine learning model at startup
load_model()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Smart Budget Manager is running"}


@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions/")
def list_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()


@app.get("/summary/")
def get_summary(db: Session = Depends(get_db)):
    total_income = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.transaction_type == "income")
        .scalar()
        or 0
    )
    total_expenses = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.transaction_type == "expense")
        .scalar()
        or 0
    )
    return {"total_income": total_income, "total_expenses": total_expenses}


@app.get("/summary/by_category")
def get_summary_by_category(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Transaction.category,
            func.sum(models.Transaction.amount).label("total_amount"),
        )
        .group_by(models.Transaction.category)
        .all()
    )
    return {category: total_amount for category, total_amount in results}


@app.get("/summary/monthly")
def get_monthly_summary(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.strftime("%Y-%m", models.Transaction.date).label("month"),
            models.Transaction.transaction_type,
            func.sum(models.Transaction.amount).label("total_amount"),
        )
        .group_by("month", models.Transaction.transaction_type)
        .all()
    )
    summary = {}
    for month, transaction_type, total_amount in results:
        if month not in summary:
            summary[month] = {"income": 0, "expense": 0}
        summary[month][transaction_type] = total_amount
    return summary


@app.get("/forecast/spending")
def forecast_spending(db: Session = Depends(get_db)):
    today = date.today()
    three_months_ago = today - timedelta(days=90)

    total_spending_last_3_months = (
        db.query(func.sum(models.Transaction.amount))
        .filter(
            models.Transaction.transaction_type == "expense",
            models.Transaction.date >= three_months_ago,
        )
        .scalar()
    )

    if total_spending_last_3_months is None:
        return {"next_month_forecast": 0}

    # Normalize to a 30-day month
    average_monthly_spending = (total_spending_last_3_months / 90) * 30

    return {"next_month_forecast": average_monthly_spending}


@app.get("/predict_category")
def get_predicted_category(name: str):
    category = predict_category(name)
    if category is None:
        raise HTTPException(
            status_code=404, detail="Model not trained yet. Please train the model first."
        )
    return {"predicted_category": category}
