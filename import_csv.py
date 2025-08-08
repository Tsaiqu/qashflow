import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product
import sys


def import_csv(file_path: str):
    df = pd.read_csv(file_path)
    db: Session = SessionLocal()
    for _, row in df.iterrows():
        if "name" in row and "category" in row and "price" in row:
            product = Product(
                name=row["name"], category=row["category"], price=row["price"]
            )
            db.add(product)
    db.commit()
    db.close()
    print("CSV import completed.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import_csv(sys.argv[1])
    else:
        import_csv("receips.csv")
