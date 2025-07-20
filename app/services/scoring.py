import json
import pandas as pd
from fuzzywuzzy import process
import joblib  

# Загрузка эталонных целей кредита
with open('data/loan_purposes.json', 'r', encoding='utf-8') as f:
    loan_purposes = json.load(f)

def match_loan_purpose(client_input: str, threshold=80):
    """Находит наиболее похожее значение цели кредита"""
    if not isinstance(client_input, str):
        return None
    matched, score = process.extractOne(client_input.strip().lower(), loan_purposes)
    return matched if score >= threshold else 'Other'

def score_new_data(X_new: pd.DataFrame):
    """
    Предсказание скоринга на новых данных с предобработкой LoanPurpose
    """
    X_new = X_new.copy()
    if 'LoanPurpose' in X_new.columns:
        X_new['LoanPurpose'] = X_new['LoanPurpose'].apply(match_loan_purpose)
        if X_new['LoanPurpose'].isnull().any():
            raise ValueError("Некоторые значения LoanPurpose не удалось сопоставить с эталонами")

    xgb_model = joblib.load("app/models/xgboost/latest.pkl")

    probs_xgb = xgb_model.predict_proba(X_new)[:, 1]

    result = pd.DataFrame({
        "xgboost_prob": probs_xgb
    }, index=X_new.index)

    return result