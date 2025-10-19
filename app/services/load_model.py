import os
import joblib

def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Путь {path} недействителен")
    return joblib.load(path)