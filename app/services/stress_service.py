# app/services/wlb_score_service.py

from app.models.ml_model import predict_wlb


def calculate_wlb_score(user_data):

    score = 100

    # Workload penalties
    score -= user_data["workload_rating"] * 4
    score -= user_data["deadline_pressure"] * 3
    score -= user_data["exhaustion_rating"] * 5

    # Task delays reduce balance
    delay_map = {
        "Never": 0,
        "Rarely": 2,
        "Sometimes": 5,
        "Often": 8,
        "Always": 12
    }

    score -= delay_map.get(user_data["task_delay"], 0)

    # Positive factors
    score += user_data["productivity_rating"] * 3
    score += user_data["social_satisfaction"] * 3
    score += user_data["travel_enjoyment"] * 2

    # Ensure range 0–100
    score = max(0, min(score, 100))

    return round(score, 2)


def get_wlb_analysis(user_data):

    # 1️⃣ Calculate WLB score
    wlb_score = calculate_wlb_score(user_data)

    # 2️⃣ Predict label using ML
    prediction = predict_wlb(user_data)

    return {
        "wlb_score": wlb_score,
        "wlb_label": prediction["wlb_label"],
        "confidence": prediction["confidence"]
    }