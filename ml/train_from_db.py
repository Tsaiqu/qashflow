from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

from models import Product


MODEL_PATH = Path(__file__).resolve().parent / "model_dump" / "model.joblib"


def train_model(db):
    products = db.query(Product).all()
    if len(products) < 2:
        raise ValueError("Not enough data to train the model!")

    # Dummy features: just index as time
    x = np.array([[i] for i in range(len(products))])
    y = np.array([p.price for p in products])

    model = LinearRegression()
    model.fit(x, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model
