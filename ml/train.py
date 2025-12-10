import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib
import os


def train_model(data_path="data/transactions.csv"):
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Skipping training.")
        return

    df = pd.read_csv(data_path)
    if "name" not in df.columns or "category" not in df.columns:
        print("CSV must contain 'name' and 'category' columns. Skipping training.")
        return

    X = df["name"]
    y = df["category"]

    model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    model.fit(X, y)

    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model, "ml/models/category_classifier.joblib")
    print("Model training completed and saved.")


if __name__ == "__main__":
    train_model()