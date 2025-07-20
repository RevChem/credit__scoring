# uvicorn app.api.v1.main:app --reload

from fastapi import FastAPI
from app.api.v1.routes.scoring import router as router_dreif
from app.api.v1.routes.predict import router as router_predict


app = FastAPI(
    title="Credit Scoring API",
    version="1.0.0",
    description="API для скоринга и переобучения моделей",
)

@app.get("/")
def home_page():
    return {"message": "Привет!"}

app.include_router(router_dreif)
app.include_router(router_predict)