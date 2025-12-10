import joblib
import os

model = None


def load_model(model_path="ml/models/category_classifier.joblib"):
    global model
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        print(f"Model not found at {model_path}. Category prediction will not be available.")


def predict_category(name: str):
    if model is None:
        return None
    return model.predict([name])[0]


load_model()