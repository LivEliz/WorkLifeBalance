# app/services/stress_service.py

from app.models.ml_model import predict_stress

def get_stress_analysis(user_data):

    ml_input = {
        "Work_Hours_Per_Week": user_data["weekly_hours"],
        "Overtime_Hours": user_data["overtime_hours"],
        "Employee_Satisfaction_Score": user_data["satisfaction_score"],
        "Projects_Handled": user_data["projects_handled"],
        "Sick_Days": user_data["sick_days"],
        "Performance_Score": user_data["projects_handled"]  # temporary mapping
    }

    stress_level, stress_percentage = predict_stress(ml_input)

    return {
        "stress_level": stress_level,
        "stress_percentage": stress_percentage
    }