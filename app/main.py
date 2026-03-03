# app/main.py
from fastapi import FastAPI
from app.models.schemas import StressInput
from app.services.stress_service import get_stress_analysis

app = FastAPI()

@app.post("/analyze")
def analyze(input_data: StressInput):
    return get_stress_analysis(input_data)

from app.database.mongo import users_collection

from datetime import datetime
from app.database.mongo import users_collection
from app.models.schemas import UserSignup

@app.post("/signup")
def signup(user: UserSignup):

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        return {"error": "User already exists"}

    user_data = {
        "email": user.email,
        "password": user.password,  # ⚠ later we will hash this
        "work_field": user.work_field,
        "normal_work_hours": user.normal_work_hours,
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user_data)

    return {"message": "User created successfully"}

from app.models.schemas import WeeklyUpdate
from app.database.mongo import weekly_logs_collection, users_collection
from datetime import datetime
from app.services.stress_service import get_stress_analysis

@app.post("/weekly-update")
def weekly_update(data: WeeklyUpdate):

    # Check if user exists
    user = users_collection.find_one({"email": data.email})
    if not user:
        return {"error": "User not found"}

    # Run ML prediction
    stress_result = get_stress_analysis(data.dict())

    # Save weekly log
    weekly_data = {
        "email": data.email,
        "weekly_hours": data.weekly_hours,
        "overtime_hours": data.overtime_hours,
        "satisfaction_score": data.satisfaction_score,
        "projects_handled": data.projects_handled,
        "sleep_hours": data.sleep_hours,
        "sick_days": data.sick_days,
        "stress_score": stress_result["stress_percentage"],
        "stress_label": stress_result["stress_level"],
        "created_at": datetime.utcnow()
    }

    weekly_logs_collection.insert_one(weekly_data)

    return stress_result
"""    
from fastapi import FastAPI
from app.services.stress_service import get_stress_analysis
from app.services.rag_service import get_recommendations

app = FastAPI()

@app.post("/analyze")
def analyze(user_data: dict):

    stress_result = get_stress_analysis(user_data)

    recommendations = get_recommendations(
        user_data,
        stress_result["stress_level"],
        stress_result["stress_percentage"]
    )

    return {
        "stress_level": stress_result["stress_level"],
        "stress_percentage": stress_result["stress_percentage"],
        "recommendations": recommendations
    }
    """