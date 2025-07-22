# uvicorn app.api.v1.main:app --reload
import os
import logging
import logging.config
import yaml

from fastapi import FastAPI
from app.users.router import router as router_users
from app.api.v1.routes.dreif import router as router_dreif
from app.api.v1.routes.predict import router as router_predict
from app.api.v1.routes.mlflow_router import router as router_mlflow

app = FastAPI(
    title="Credit Scoring API",
    description="API для скоринга и обучения моделей",
)

@app.get("/")
def home_page():
    return {"message": "Привет!"}


app.include_router(router_users)
app.include_router(router_dreif)
app.include_router(router_predict)
app.include_router(router_mlflow)


config_path = os.path.join(os.path.dirname(__file__), "logging_config.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.info("Логирование запущено!")