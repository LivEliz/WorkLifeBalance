# app/services/wlb_score_service.py

from app.models.ml_model import predict_wlb

# ------------------------------
# Numeric helpers (same as dataset generator)
# ------------------------------

hours_score = {"<35":35,"35-40":38,"40-45":43,"45-50":48,">50":55}
overtime_score = {"None":0,"1-5":3,"6-10":8,"11-15":13,">15":18}
projects_score = {"1":1,"2-3":3,"4-5":5,"6-8":7,">8":9}
meetings_score = {"0-5":3,"6-10":8,"11-15":13,"16-20":18,">20":25}
breaks_score = {"None":0,"1":1,"2":2,"3":3,"4+":4}
family_score = {"<3":2,"3-5":4,"6-10":8,"11-15":12,">15":16}


def calculate_wlb_score(user_data):

    score = 100

    # Work intensity penalties
    score -= max(0, hours_score[user_data["hours_worked"]] - 40) * 1.5
    score -= overtime_score[user_data["overtime_hours"]] * 2
    score -= projects_score[user_data["projects_handled"]] * 1.2
    score -= meetings_score[user_data["meetings_count"]] * 1

    # Stress factors
    score -= user_data["workload_rating"] * 4
    score -= user_data["deadline_pressure"] * 4
    score -= user_data["exhaustion_rating"] * 5

    # Sick leave impact
    sick_days = user_data.get("sick_days", "None")
    sick_days_num = 0 if sick_days == "None" else int(sick_days.replace("+",""))
    score -= sick_days_num * 4

    # Positive balance factors
    score += breaks_score[user_data["breaks"]] * 1
    score += family_score[user_data["family_time"]] * 0.7
    score += user_data["social_satisfaction"] * 1
    score += user_data["productivity_rating"] * 0.5
    score += user_data["travel_enjoyment"] * 0.2

    # Ensure range
    score = max(0, min(100, int(score)))

    return score


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