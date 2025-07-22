from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io
from app.services.drift_detection import detect_drift, generate_drift_report_html


router = APIRouter(prefix="/data", tags=["Дрейф признаков"])

@router.post("/drift", summary="Дрейф признаков")
async def drift(
    reference: UploadFile = File(..., description="Файл с эталонными данными"),
    current: UploadFile = File(..., description="Файл с текущими данными")
):
    try:
        df_ref = pd.read_csv(io.BytesIO(await reference.read()))
        df_cur = pd.read_csv(io.BytesIO(await current.read()))

        generate_drift_report_html(df_ref, df_cur, output_path="drift_report.html")

        result = detect_drift(df_ref, df_cur)
        result["report_path"] = "drift_report.html"
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


