from fastapi import HTTPException
import pandas as pd
import joblib
import json
from fuzzywuzzy import process
from fastapi import APIRouter
from app.users.schemas import SUser
from app.users.sql_enums import JobType


router = APIRouter(prefix="/predict", tags=["Предсказание для одного клиента"])

# Загрузка эталонных целей кредита
with open('data/loan_purposes.json', 'r', encoding='utf-8') as f:
    loan_purposes = json.load(f)

# Загрузка списка признаков, на которых обучалась модель
with open('data/dataset_columns.json', 'r', encoding='utf-8') as f:
    dataset_columns = json.load(f)

# Загрузка модели
try:
    xgb_model = joblib.load("models/xgboost/latest.pkl")
except FileNotFoundError:
    raise Exception("Модель xgb_model.pkl не найдена")

# Функция fuzzy-сопоставления
def match_loan_purpose(client_input: str, threshold=80):
    if not isinstance(client_input, str):
        return None
    matched, score = process.extractOne(client_input.strip().lower(), loan_purposes)
    return matched if score >= threshold else None


@router.post("/predict")
def predict(data: SUser):
    try:
        df = pd.DataFrame([data.dict()])

        JOB_TYPE_MAP = {
            "Employed - full time": JobType.FULL_TIME,
            "Employed - part time": JobType.PART_TIME,
            "Self employed": JobType.SELF_EMPLOYED,
            "Retired": JobType.RETIRED
        }

        df['EmpPT'] = df['EmpPT'].map(JOB_TYPE_MAP)


        # 1. Обработка LoanPurpose
        df['LoanPurpose'] = df['LoanPurpose'].apply(match_loan_purpose)
        if df['LoanPurpose'].isnull().any():
            raise HTTPException(status_code=400, detail="Не удалось сопоставить LoanPurpose")

        # 2. One-hot кодирование LoanPurpose
        df = pd.get_dummies(df, columns=['LoanPurpose'], prefix='LoanPurpose')

        # 3. Добавляем недостающие one-hot столбцы, если они есть в модели
        for col in dataset_columns:
            if col not in df.columns:
                df[col] = 0

        # 4. Переставляем и приводим типы к порядку, в котором обучалась модель
        df = df[dataset_columns].fillna(0).astype({col: 'int64' for col in dataset_columns if col.startswith('LoanPurpose_')})

        # 5. Предсказание
        prob = xgb_model.predict_proba(df)[0][1]

        return {
            "probability": float(prob),
            "risk_category": "high" if prob > 0.5 else "low"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")
    








