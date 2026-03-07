# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import (
    UserSignup,
    UserProfile,
    WeeklyCheckin
)

from app.services.stress_service import get_wlb_analysis
from app.services.llm_service import generate_recommendations

from app.database.mongo import (
    users_collection,
    weekly_logs_collection,
    wlb_results_collection
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
# SIGNUP
# =========================

@app.post("/signup")
def signup(user: UserSignup):

    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "password": user.password,
        "created_at": datetime.utcnow()
    })

    token = create_access_token({"email": user.email})

    return {"message": "User created successfully",
            "access_token": token,
            "token_type": "bearer"
    }


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

    if existing_user["password"] != user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"email": user.email})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# PROFILE QUESTIONNAIRE
# =========================

@app.post("/profile-setup")
def profile_setup(
    profile: UserProfile,
    current_user: str = Depends(get_current_user)
):

    if current_user != profile.email:
        raise HTTPException(status_code=403, detail="Unauthorized")

    users_collection.update_one(
        {"email": profile.email},
        {"$set": profile.dict()}
    )

    return {"message": "Profile saved successfully"}


# =========================
# WEEKLY CHECKIN
# =========================
@app.post("/weekly-checkin")
def weekly_checkin(
    data: WeeklyCheckin,
    current_user: str = Depends(get_current_user)
):

    if current_user != data.email:
        raise HTTPException(status_code=403, detail="Unauthorized")

    user = users_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ------------------------------------------------
    # Prepare ML Model Input
    # ------------------------------------------------
    break_map = {
        "Less than 10 minutes":"<10",
        "10 – 20 minutes":"10-20",
        "20 – 30 minutes":"20-30",
        "30 – 45 minutes":"30-45",
        "More than 45 minutes":">45"
        }

    travel_map = {
        "No travel":"No travel",
        "1 trip":"1 trip",
        "2 trips":"2 trips",
        "3 trips":"3 trips",
        "More than 3 trips":">3 trips"
        }
    ml_input = {
        "hours_worked": data.hours_worked,
        "overtime_hours": data.overtime_hours,
        "projects_handled": data.projects_handled,
        "meetings_count": data.meetings_count,

        "workload_rating": data.workload_rating,
        "deadline_pressure": data.deadline_pressure,

        "productivity_rating": data.productivity_rating,
        "task_delay": data.task_delay,

        "breaks": data.breaks,
        "break_duration": break_map[data.break_duration],


        "sick_days": data.sick_days,
        "leave_days": data.leave_days,
        "exhaustion_rating": data.exhaustion_rating,

        "travel": travel_map[data.travel],
        "travel_enjoyment": data.travel_enjoyment,

        "family_time": data.family_time,
        "social_satisfaction": data.social_satisfaction,

        # From profile setup
        "commute_time": user.get("commute_time")
    }

    # ------------------------------------------------
    # ML Prediction
    # ------------------------------------------------

    wlb_result = get_wlb_analysis(ml_input)

    # ------------------------------------------------
    # LLM Recommendation Input
    # ------------------------------------------------

    llm_input = {

        # Profile info
        "name": user.get("name"),
        "age": user.get("age"),
        "department": user.get("department"),
        "role_level": user.get("role_level"),
        "work_mode": user.get("work_mode"),
        "commute_time": user.get("commute_time"),

        # Weekly checkin
        **data.dict(),

        # ML output
        "wlb_score": wlb_result["wlb_score"],
        "wlb_label": wlb_result["wlb_label"],
        "confidence": wlb_result["confidence"]
    }

    ai_output = generate_recommendations(llm_input)

    # ------------------------------------------------
    # Save Weekly Log
    # ------------------------------------------------

    weekly_logs_collection.insert_one({
        **data.dict(),
        "wlb_score": wlb_result["wlb_score"],
        "wlb_label": wlb_result["wlb_label"],
        "confidence": wlb_result["confidence"],
        "recommendations": ai_output.get("recommendations"),
        "weekly_checklist": ai_output.get("weekly_checklist"),
        "created_at": datetime.utcnow()
    })

    # Store ML result separately

    wlb_results_collection.insert_one({
        "email": data.email,
        "wlb_score": wlb_result["wlb_score"],
        "wlb_label": wlb_result["wlb_label"],
        "confidence": wlb_result["confidence"],
        "created_at": datetime.utcnow()
    })

    # ------------------------------------------------
    # API Response
    # ------------------------------------------------

    return {
        "wlb_score": wlb_result["wlb_score"],
        "wlb_label": wlb_result["wlb_label"],
        "confidence": wlb_result["confidence"],
        "recommendations": ai_output.get("recommendations"),
        "weekly_checklist": ai_output.get("weekly_checklist")
    }


# =========================
# WLB TREND
# =========================

@app.get("/wlb-trend")
def wlb_trend(current_user: str = Depends(get_current_user)):

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

    scores = [log["wlb_score"] for log in logs]

    current_score = scores[-1]
    previous_score = scores[-2]

    change = round(current_score - previous_score, 2)

    if change > 0:
        trend = "Improving"
    elif change < 0:
        trend = "Declining"
    else:
        trend = "Stable"

    return {
        "current_wlb_score": current_score,
        "previous_wlb_score": previous_score,
        "change": change,
        "trend": trend,
        "total_weeks_tracked": len(scores),
        "last_5_weeks": scores[-5:]
    }


# =========================
# DELETE ACCOUNT
# =========================

@app.delete("/delete-account")
def delete_account(current_user: str = Depends(get_current_user)):

    users_collection.delete_one({"email": current_user})
    weekly_logs_collection.delete_many({"email": current_user})
    wlb_results_collection.delete_many({"email": current_user})

    return {"message": "Account deleted successfully"}