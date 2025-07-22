from fastapi import APIRouter, Form
import numpy as np
import shap

router = APIRouter(prefix="/interpretation", tags=["Интерпретация предсказания для одного клиента"])

@router.post("/interpretation/{id}")
async def interpretation(
    id: int = Form(....)
):
try:
    explainer = shap.Explainer(best_model, X_train_bal)
    expected_value = explainer.expected_value
    shap_values = explainer(X_test)
    
    top10 = np.abs(shap_values[id].values).argsort()[-10:][::-1]
    shap.force_plot(expected_value, shap_values[id].values[top10], X_train.iloc[10][top10])
