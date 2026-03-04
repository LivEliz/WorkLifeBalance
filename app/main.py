# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.models.schemas import StressInput, UserSignup, WeeklyUpdate
from app.services.stress_service import get_stress_analysis
from app.services.llm_service import generate_recommendations
from app.database.mongo import users_collection, weekly_logs_collection

app = FastAPI()

# =========================
# JWT CONFIG
# =========================
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# =========================
# ANALYZE (UNPROTECTED)
# =========================
@app.post("/analyze")
def analyze(input_data: StressInput):
    return get_stress_analysis(input_data)


# =========================
# SIGNUP
# =========================
@app.post("/signup")
def signup(user: UserSignup):

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        return {"error": "User already exists"}

    user_data = {
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "password": user.password,  # simple compare (no hashing)
        "work_field": user.work_field,
        "normal_sleep_hours": user.normal_sleep_hours,
        "normal_work_hours": user.normal_work_hours,
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(user_data)

    return {"message": "User created successfully"}


# =========================
# LOGIN
# =========================
from pydantic import BaseModel

class LoginInput(BaseModel):
    email: str
    password: str


@app.post("/login")
def login(user: LoginInput):

    existing_user = users_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")

    # Simple string comparison
    if existing_user["password"] != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"email": user.email})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# WEEKLY UPDATE (PROTECTED)
# =========================
@app.post("/weekly-update")
def weekly_update(
    data: WeeklyUpdate,
    current_user: str = Depends(get_current_user)
):

    # Ensure token email matches request email
    if current_user != data.email:
        raise HTTPException(status_code=403, detail="Unauthorized action")

    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ML prediction
    stress_result = get_stress_analysis(data.dict())

    # Prepare LLM input
    llm_input = {
        "stress_level": stress_result["stress_level"],
        "stress_percentage": stress_result["stress_percentage"],
        "Work_Hours_Per_Week": data.weekly_hours,
        "Overtime_Hours": data.overtime_hours,
        "Employee_Satisfaction_Score": data.satisfaction_score,
        "Projects_Handled": data.projects_handled,
        "Sick_Days": data.sick_days,
        "Performance_Score": 3,
        "name": user.get("name"),
        "age": user.get("age"),
        "work_field": user.get("work_field"),
        "normal_sleep_hours": user.get("normal_sleep_hours"),
        "normal_work_hours": user.get("normal_work_hours")
    }

    ai_output = generate_recommendations(llm_input)

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
        "recommendations": ai_output.get("recommendations"),
        "weekly_checklist": ai_output.get("weekly_checklist"),
        "created_at": datetime.utcnow()
    }

    weekly_logs_collection.insert_one(weekly_data)

    return {
        "stress_level": stress_result["stress_level"],
        "stress_percentage": stress_result["stress_percentage"],
        "recommendations": ai_output.get("recommendations"),
        "weekly_checklist": ai_output.get("weekly_checklist")
    }


# =========================
# DELETE ACCOUNT (PROTECTED)
# =========================
@app.delete("/delete-account")
def delete_account(current_user: str = Depends(get_current_user)):

    users_collection.delete_one({"email": current_user})
    weekly_logs_collection.delete_many({"email": current_user})

    return {"message": "Account deleted successfully"}

@app.get("/stress-trend")
def stress_trend(current_user: str = Depends(get_current_user)):

    # Fetch all weekly logs for the user
    logs = list(
        weekly_logs_collection
        .find({"email": current_user})
        .sort("created_at", 1)
    )

    if len(logs) < 2:
        return {
            "message": "Not enough data to calculate trend",
            "data_points": len(logs)
        }

    # Extract stress scores
    stress_scores = [log["stress_score"] for log in logs]

    current_stress = stress_scores[-1]
    previous_stress = stress_scores[-2]

    change = round(current_stress - previous_stress, 2)

    if change > 0:
        trend = "Increasing"
    elif change < 0:
        trend = "Decreasing"
    else:
        trend = "Stable"

    return {
        "current_stress": current_stress,
        "previous_stress": previous_stress,
        "change": change,
        "trend": trend,
        "total_weeks_tracked": len(stress_scores),
        "last_5_weeks": stress_scores[-5:]
    }