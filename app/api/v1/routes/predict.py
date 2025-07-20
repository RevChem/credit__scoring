from fastapi import HTTPException
import pandas as pd
import joblib
import json
from fuzzywuzzy import process
from fastapi import APIRouter, Depends
from app.users.schemas import SUser
from app.users.sql_enums import JobType
from app.users.models import User
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


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
async def predict(data: SUser, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Преобразуем входные данные в DataFrame
        df = pd.DataFrame([data.model_dump()])

        JOB_TYPE_MAP = {
            "Employed - full time": JobType.FULL_TIME,
            "Employed - part time": JobType.PART_TIME,
            "Self employed": JobType.SELF_EMPLOYED,
            "Retired": JobType.RETIRED
        }

        df['EmpPT'] = df['EmpPT'].map(JOB_TYPE_MAP)

        # 3. Обработка LoanPurpose через fuzzywuzzy
        df['LoanPurpose'] = df['LoanPurpose'].apply(match_loan_purpose)
        if df['LoanPurpose'].isnull().any():
            raise HTTPException(status_code=400, detail="Не удалось сопоставить LoanPurpose")

        # 4. One-hot кодирование
        df = pd.get_dummies(df, columns=['LoanPurpose'], prefix='LoanPurpose')

        # 5. Добавляем недостающие one-hot столбцы
        for col in dataset_columns:
            if col not in df.columns:
                df[col] = 0

        # 6. Приводим к нужному порядку и типам
        df = df[dataset_columns].fillna(0).astype({col: 'int64' for col in dataset_columns if col.startswith('LoanPurpose_')})

        # 7. Предсказание
        prob = xgb_model.predict_proba(df)[0][1]
        risk_category = "high" if prob > 0.5 else "low"

        # 8. Сохранение в БД
        db_user = User(
            Amt=data.Amt,
            Trm=data.Trm,
            YngAcntAge=data.YngAcntAge,
            CntActv=data.CntActv,
            CntCls12=data.CntCls12,
            CntOpn12=data.CntOpn12,
            CntSttl=data.CntSttl,
            AvgAcntAge=data.AvgAcntAge,
            OutBal=data.OutBal,
            OutBalNoMtg=data.OutBalNoMtg,
            WorstPayStat=data.WorstPayStat,
            EmpPT=data.EmpPT,  
            EmpRtrd=data.EmpRtrd,
            EmpSelf=data.EmpSelf,
            LoanPurpose=data.LoanPurpose,
            Probability=prob,
            Risk_Category=risk_category
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return {
            "probability": float(prob),
            "risk_category": risk_category
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")







