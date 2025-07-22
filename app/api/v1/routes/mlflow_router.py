import mlflow
from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np

router = APIRouter(prefix="/mlflow_router", tags=["Mlflow"])

mlflow.set_tracking_uri("http://localhost:5000")
model = mlflow.pyfunc.load_model("models:/Credit_Scoring/latest")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: list[float]


@router.post("/predict", response_model=PredictionResponse, 
             summary="Получение предсказания из последней лучшей обученной модели Mlflow")
def predict(request: PredictionRequest):
    input_data = np.array([request.features])
    pred_proba = model.predict(input_data)[0]
    pred_class = int(pred_proba >= 0.5)
    return {
        "prediction": pred_class,
        "probability": [1 - pred_proba, pred_proba]
    }


@router.get("/model-info", summary="Информация о последней лучшей обученной модели Mlflow")
def model_info():
    client = mlflow.tracking.MlflowClient()
    latest_version = client.get_latest_versions("Credit_Scoring", stages=["Production", "None"])[0]
    
    run_id = latest_version.run_id
    run = client.get_run(run_id)
    
    return {
        "model_name": latest_version.name,
        "version": latest_version.version,
        "run_id": run_id,
        "metrics": run.data.metrics,
        "params": run.data.params,
        "status": latest_version.current_stage
    }