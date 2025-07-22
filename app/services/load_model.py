import os
import joblib

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Модель не найдена: {model_path}")
    return joblib.load(model_path)