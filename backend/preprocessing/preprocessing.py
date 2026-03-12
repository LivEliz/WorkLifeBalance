import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "wlb_score_dataset.csv")

df = pd.read_csv(DATA_PATH)

print("Original dataset:", df.shape)

# -------------------------------------------------
# Clean dataset
# -------------------------------------------------

df.replace(["01-01-2000", "01/01/2000"], np.nan, inplace=True)

numeric_cols = [
"DAILY_STRESS",
"TODO_COMPLETED",
"FLOW",
"SLEEP_HOURS",
"PLACES_VISITED",
"CORE_CIRCLE",
"ACHIEVEMENT",
"SUPPORTING_OTHERS",
"TIME_FOR_PASSION",
"DAILY_SHOUTING",
"LOST_VACATION",
"WORK_LIFE_BALANCE_SCORE"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# -------------------------------------------------
# Keep Kaggle Score
# -------------------------------------------------

df["wlb_score"] = df["WORK_LIFE_BALANCE_SCORE"]

def label(score):
    if score < 550:
        return "POOR"
    elif score < 700:
        return "MODERATE"
    else:
        return "GOOD"

df["wlb_label"] = df["wlb_score"].apply(label)

# -------------------------------------------------
# Feature Engineering
# -------------------------------------------------

# HOURS WORKED (proxy using TODO_COMPLETED)

df["hours_worked"] = pd.cut(
    df["TODO_COMPLETED"],
    bins=[-1,2,4,6,8,10],
    labels=["<35","35-40","40-45","45-50",">50"]
)

# OVERTIME HOURS (proxy using DAILY_STRESS)

df["overtime_hours"] = pd.cut(
    df["DAILY_STRESS"],
    bins=[-1,1,3,5,7,10],
    labels=["None","1-5","6-10","11-15",">15"]
)

# PROJECTS HANDLED (TODO_COMPLETED)

df["projects_handled"] = pd.cut(
    df["TODO_COMPLETED"],
    bins=[-1,1,3,5,8,10],
    labels=["1","2-3","4-5","6-8",">8"]
)

# MEETINGS COUNT (FLOW proxy)

df["meetings_count"] = pd.cut(
    df["FLOW"],
    bins=[-1,2,4,6,8,10],
    labels=["0-5","6-10","11-15","16-20",">20"]
)

# WORKLOAD RATING

df["workload_rating"] = df["DAILY_STRESS"].clip(1,5)

# DEADLINE PRESSURE (mapped from DAILY_SHOUTING)

df["deadline_pressure"] = (
    df["DAILY_SHOUTING"] / 10 * 5
).round().clip(1,5)

# PRODUCTIVITY RATING (mapped from ACHIEVEMENT)

df["productivity_rating"] = (
    df["ACHIEVEMENT"] / 10 * 5
).round().clip(1,5)

# TASK DELAY (from DAILY_STRESS)

df["task_delay"] = pd.cut(
    df["DAILY_STRESS"],
    bins=[-1,1,3,5,7,10],
    labels=["Never","Rarely","Sometimes","Often","Always"]
)

# BREAKS (from SLEEP_HOURS)

df["breaks"] = pd.cut(
    df["SLEEP_HOURS"],
    bins=[-1,4,5,6,7,24],
    labels=["None","1","2","3","4+"]
)

# BREAK DURATION (from FLOW)

df["break_duration"] = pd.cut(
    df["FLOW"],
    bins=[-1,2,4,6,8,10],
    labels=["<10","10-20","20-30","30-45",">45"]
)

# SICK DAYS (from LOST_VACATION)

df["sick_days"] = pd.cut(
    df["LOST_VACATION"],
    bins=[-1,0,2,4,6,10],
    labels=["None","1","2","3","4+"]
)

# LEAVE DAYS (from LOST_VACATION)

df["leave_days"] = pd.cut(
    df["LOST_VACATION"],
    bins=[-1,1,3,5,7,10],
    labels=["None","1","2","3","4+"]
)

# EXHAUSTION RATING (from DAILY_STRESS)

df["exhaustion_rating"] = (
    df["DAILY_STRESS"] / 10 * 5
).round().clip(1,5)

# TRAVEL (from PLACES_VISITED)

df["travel"] = pd.cut(
    df["PLACES_VISITED"],
    bins=[-1,0,2,4,6,10],
    labels=["No travel","1 trip","2 trips","3 trips",">3 trips"]
)

# TRAVEL ENJOYMENT (from TIME_FOR_PASSION)

df["travel_enjoyment"] = (
    df["TIME_FOR_PASSION"] / 10 * 5
).round().clip(1,5)

# FAMILY TIME (from CORE_CIRCLE)

df["family_time"] = pd.cut(
    df["CORE_CIRCLE"],
    bins=[-1,2,4,6,8,20],
    labels=["<3","3-5","6-10","11-15",">15"]
)

# SOCIAL SATISFACTION (from SUPPORTING_OTHERS)

df["social_satisfaction"] = (
    df["SUPPORTING_OTHERS"] / 10 * 5
).round().clip(1,5)

# COMMUTE TIME (synthetic because dataset lacks it)

np.random.seed(42)

df["commute_time"] = np.random.choice(
    ["No commute","<30","30-60","1-2h",">2h"],
    len(df)
)

# -------------------------------------------------
# Final dataset
# -------------------------------------------------

columns = [

"hours_worked",
"overtime_hours",
"projects_handled",
"meetings_count",
"workload_rating",
"deadline_pressure",
"productivity_rating",
"task_delay",
"breaks",
"break_duration",
"sick_days",
"leave_days",
"exhaustion_rating",
"travel",
"travel_enjoyment",
"family_time",
"social_satisfaction",
"commute_time",

"wlb_score",
"wlb_label"

]

df_final = df[columns]

SAVE_PATH = os.path.join(PROJECT_ROOT,"data","processed_wlb_dataset.csv")

df_final.to_csv(SAVE_PATH,index=False)

print("Processed dataset:",df_final.shape)