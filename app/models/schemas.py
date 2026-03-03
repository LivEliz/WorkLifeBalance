from pydantic import BaseModel

class StressInput(BaseModel):
    work_field: str
    normal_hours: float
    weekly_hours: float
    overtime_hours: float
    satisfaction_score: float
    projects_handled: int
    sleep_hours: float
    sick_days: int

from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    work_field: str
    normal_work_hours: float

class WeeklyUpdate(BaseModel):
    email: EmailStr   # identify user
    weekly_hours: float
    overtime_hours: float
    satisfaction_score: float
    projects_handled: int
    sleep_hours: float
    sick_days: int