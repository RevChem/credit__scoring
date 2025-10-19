from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io
from app.services.drift import detect, drift_report


router = APIRouter(prefix="/data", tags=["Дрейф признаков"])

@router.post("/drift", summary="Дрейф признаков")
def drift(
    ref: UploadFile = File(..., description="Эталонные данные"),
    cur: UploadFile = File(..., description="Текущие данные")
):
    ref = pd.read_csv(io.BytesIO(ref.file.read()))
    cur = pd.read_csv(io.BytesIO(cur.file.read()))

    drift_report(ref, cur, output_path="report.html")

    result = detect(ref, cur)
    result["report_path"] = "report.html"
    return JSONResponse(content=result)
