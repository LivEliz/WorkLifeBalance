import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "wlb_score_dataset.csv")

df = pd.read_csv(DATA_PATH)


df.replace(["01-01-2000","01/01/2000","2000-01-01"], np.nan, inplace=True)
print("Original dataset:", df.shape)
# -------------------------------------------------
# Convert numeric columns
# -------------------------------------------------

numeric_cols = [
"DAILY_STRESS",
"TODO_COMPLETED",
"FLOW",
"SLEEP_HOURS",
"SOCIAL_NETWORK",
"CORE_CIRCLE",
"PLACES_VISITED",
"WORK_LIFE_BALANCE_SCORE"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# -------------------------------------------------
# Keep ORIGINAL Kaggle Score
# -------------------------------------------------

df["wlb_score"] = df["WORK_LIFE_BALANCE_SCORE"]

# -------------------------------------------------
# Create label from score
# -------------------------------------------------

def label(score):
    if score < 550:
        return "POOR"
    elif score < 700:
        return "MODERATE"
    else:
        return "GOOD"

df["wlb_label"] = df["wlb_score"].apply(label)

# -------------------------------------------------
# Feature engineering
# -------------------------------------------------

df["workload_rating"] = df["DAILY_STRESS"].clip(1,5)

df["productivity_rating"] = (
df["TODO_COMPLETED"]/df["TODO_COMPLETED"].max()*5
).round().clip(1,5)

df["social_satisfaction"] = (
df["SOCIAL_NETWORK"]/df["SOCIAL_NETWORK"].max()*5
).round().clip(1,5)

df["family_time"] = pd.cut(
df["CORE_CIRCLE"],
bins=[-1,2,4,6,8,10],
labels=["<3","3-5","6-10","11-15",">15"]
)

df["exhaustion_rating"] = (
df["DAILY_STRESS"]*0.7 +
(10-df["SLEEP_HOURS"])*0.3
).round().clip(1,5)

df["breaks"] = pd.cut(
df["SLEEP_HOURS"],
bins=[-1,5,6,7,8,24],
labels=["None","1","2","3","4+"]
)

df["break_duration"] = pd.cut(
df["FLOW"],
bins=[-1,1,2,3,4,5],
labels=["<10","10-20","20-30","30-45",">45"]
)

df["task_delay"] = pd.cut(
df["DAILY_STRESS"],
bins=[-1,1,2,3,4,5],
labels=["Never","Rarely","Sometimes","Often","Always"]
)

df["travel_enjoyment"] = (
df["PLACES_VISITED"]/df["PLACES_VISITED"].max()*5
).round().clip(1,5)

categorical_cols = [
"family_time",
"breaks",
"break_duration",
"task_delay"
]

for col in categorical_cols:
    df[col] = df[col].astype(str)

# -------------------------------------------------
# Synthetic questionnaire compatible columns
# -------------------------------------------------

np.random.seed(42)

df["hours_worked"] = np.random.choice(["<35","35-40","40-45","45-50",">50"],len(df))
df["overtime_hours"] = np.random.choice(["None","1-5","6-10","11-15",">15"],len(df))
df["projects_handled"] = np.random.choice(["1","2-3","4-5","6-8",">8"],len(df))
df["meetings_count"] = np.random.choice(["0-5","6-10","11-15","16-20",">20"],len(df))
df["sick_days"] = np.random.choice(["None","1","2","3","4+"],len(df))
df["leave_days"] = np.random.choice(["None","1","2","3","4+"],len(df))
df["travel"] = np.random.choice(["No travel","1 trip","2 trips","3 trips",">3 trips"],len(df))
df["commute_time"] = np.random.choice(["No commute","<30","30-60","1-2h",">2h"],len(df))

df["deadline_pressure"] = df["workload_rating"]

# -------------------------------------------------
# Final dataset
# -------------------------------------------------
df = df.fillna("Unknown")

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