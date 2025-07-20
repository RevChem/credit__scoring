from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io


from app.services.drift_detection import detect_drift, generate_drift_report_html
#from app.services.model_loader import load_model
#from app.services.scoring import make_prediction
#from app.services.retraining import retrain_model  

router = APIRouter(prefix="/data", tags=["Дрейф признаков"])

@router.post("/drift")
async def drift(
    reference: UploadFile = File(..., description="Файл с эталонными данными"),
    current: UploadFile = File(..., description="Файл с текущими данными")
):
    try:
        df_ref = pd.read_csv(io.BytesIO(await reference.read()))
        df_cur = pd.read_csv(io.BytesIO(await current.read()))

        # Генерация HTML-отчета
        generate_drift_report_html(df_ref, df_cur, output_path="drift_report.html")

        result = detect_drift(df_ref, df_cur)
        result["report_path"] = "drift_report.html"
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})





# Модель входных данных
# class InputData(BaseModel):
#     data: List[dict]


# @router.post("/predict")
# def predict(input_data: InputData):
#     try:
#         df = pd.DataFrame(input_data.data)
#         model = load_model()
#         predictions = make_prediction(model, df)
#         return {"predictions": predictions.tolist()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/retrain")
# def retrain():
#     try:
#         retrain_model()  # функция переобучения модели
#         return {"message": "Model retrained and saved successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
