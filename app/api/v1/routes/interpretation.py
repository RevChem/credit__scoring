from fastapi import APIRouter
import numpy as np
import shap

router = APIRouter(prefix="/interpretation", tags=["Интерпретация предсказания для одного клиента"])

@router.post("/interpretation/{client_id}")
def interpretation(
    client_id: int
):
    try:
        explainer = shap.Explainer(best_model, X_train_bal)
        expected_value = explainer.expected_value
        shap_values = explainer(X_test)

        top10 = np.abs(shap_values[client_id].values).argsort()[-10:][::-1]
        plot = shap.force_plot(expected_value, shap_values[client_id].values[top10], X_test.iloc[client_id][top10])
        return {"plot": str(plot)}  
    except Exception as e:
        return {"error": str(e)}
