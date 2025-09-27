import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Transaction
import sys
from datetime import datetime
import os


def import_csv(file_path: str):
    # Create the table if it doesn't exist
    Base.metadata.create_all(bind=engine)

    if not os.path.exists(file_path):
        print(f"File not found at {file_path}. Skipping import.")
        return

    df = pd.read_csv(file_path)
    db: Session = SessionLocal()
    for _, row in df.iterrows():
        if all(
            col in row for col in ["name", "category", "amount", "date", "transaction_type"]
        ):
            transaction = Transaction(
                name=row["name"],
                category=row["category"],
                amount=row["amount"],
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                transaction_type=row["transaction_type"],
            )
            db.add(transaction)
    db.commit()
    db.close()
    print("CSV import completed.")


if __name__ == "__main__":
    # The default file path is now set to a more appropriate location
    default_path = "data/transactions.csv"
    if len(sys.argv) > 1:
        import_csv(sys.argv[1])
    else:
        import_csv(default_path)
