from sklearn.linear_model import LinearRegression
import numpy as np
from models import Product


def train_model(db):
    products = db.query(Product).all()
    if len(products) < 2:
        raise ValueError("Not enough data to train the model!")

    # Dummy features: just index as time
    x = np.array([[i] for i in range(len(products))])
    y = np.array([p.price for p in products])

    model = LinearRegression()
    model.fit(x, y)
    return model
