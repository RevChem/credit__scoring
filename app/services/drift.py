from evidently.report import Report
from evidently.metric_preset import (DataDriftPreset,
    TargetDriftPreset, ClassificationPreset)
from evidently import ColumnMapping
import pandas as pd

column = ColumnMapping(
target='Success',
    prediction='Success'  
)

def detect(
    ref: pd.DataFrame,
    cur: pd.DataFrame,
    threshold: float = 0.5,
    top_n: int = 30,
):
    report = Report(metrics=[
        DataDriftPreset(),     
        TargetDriftPreset(),  
        ClassificationPreset()
    ])
    report.run(reference_data=ref, current_data=cur, column_mapping=column)
    report_dict = report.as_dict()

    drift_results = {}

    data_drift = report_dict["metrics"][0]["result"]
    feature_drift_scores = {}
    for feature in data_drift.get("features", {}):
        score = data_drift["features"][feature].get("drift_score", 0)
        if score > threshold:
            feature_drift_scores[feature] = score
    drift_results["feature_drift"] = dict(sorted(feature_drift_scores.items(), key=lambda x: x[1], reverse=True)[:top_n])

    target_drift = report_dict["metrics"][1]["result"]
    target_drift_score = target_drift.get("drift_score", 0)
    drift_results["target_drift_score"] = target_drift_score
    drift_results["target_drift_detected"] = target_drift_score > threshold

    classification_metrics = report_dict["metrics"][2]["result"]
    drift_results["classification_metrics_ref"] = classification_metrics.get("performance", {}).get("reference", {})
    drift_results["classification_metrics_cur"] = classification_metrics.get("performance", {}).get("current", {})

    return {
        "drifted_features": drift_results["feature_drift"],
        "total_drifted_features": len(drift_results["feature_drift"]),
        "target_drift_score": drift_results["target_drift_score"],
        "target_drift_detected": drift_results["target_drift_detected"],
        "classification_metrics_ref": drift_results["classification_metrics_ref"],
        "classification_metrics_cur": drift_results["classification_metrics_cur"],
    }


def drift_report(ref: pd.DataFrame, cur: pd.DataFrame, output_path: str = "drift_report.html"):
    report = Report(metrics=[
        DataDriftPreset(),
        TargetDriftPreset(),
        ClassificationPreset(),
    ])
    report.run(reference_data=ref, current_data=cur, column_mapping=column)
    report.save_html(output_path)
    print(f"Отчет сохранён в {output_path}")
