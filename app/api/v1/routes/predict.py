from fastapi import HTTPException
import pandas as pd
from app.services.load_model import load_model
import json
from fuzzywuzzy import process
from fastapi import APIRouter, Depends
from app.users.schemas import SUser
from app.users.sql_enums import JOB_TYPE_MAP
from app.users.models import User
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/predict", tags=["Предсказание для одного клиента"])

with open('data/loan_purposes.json', 'r', encoding='utf-8') as f:
    loan_purposes = json.load(f)

with open('data/dataset_columns.json', 'r', encoding='utf-8') as f:
    dataset_columns = json.load(f)

def match_loan_purpose(client_input: str, threshold=80):
    if not isinstance(client_input, str):
        return None
    matched, score = process.extractOne(client_input.strip().lower(), loan_purposes)
    return matched if score >= threshold else None


@router.post("/predict", summary="Получение предсказания для одного клиента из последней стабильной версии")
async def predict(data: SUser, db: AsyncSession = Depends(get_db)):
    try:
        df = pd.DataFrame([data.model_dump()])

        df['EmpPT'] = df['EmpPT'].map(JOB_TYPE_MAP)

        df['LoanPurpose'] = df['LoanPurpose'].apply(match_loan_purpose)
        df['LoanPurpose'] = df['LoanPurpose'].fillna('other')
        df = pd.get_dummies(df, columns=['LoanPurpose'], prefix='LoanPurpose')

        for col in dataset_columns:
            if col not in df.columns:
                df[col] = 0

        df = df[dataset_columns].fillna(0).astype({col: 'int64' for col in dataset_columns if col.startswith('LoanPurpose_')})

        xgb_model = load_model("models/xgboost/latest.pkl")
        prob = xgb_model.predict_proba(df)[0][1]
        risk_category = "high" if prob > 0.5 else "low"

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







