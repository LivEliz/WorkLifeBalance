print("=== ML MODEL MODULE LOADED ===")

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go TWO levels up (models → app → project root)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "clean_employee_data.csv")

df = pd.read_csv(DATA_PATH)

# -------------------------------------------------
# 1️⃣ Normalize Satisfaction & Performance (1–5 → 0–1)
# -------------------------------------------------

sat_perf_scaler = MinMaxScaler()
df[["Employee_Satisfaction_Score", "Performance_Score"]] = \
    sat_perf_scaler.fit_transform(
        df[["Employee_Satisfaction_Score", "Performance_Score"]]
    )

# -------------------------------------------------
# 2️⃣ Normalize workload features ONLY for stress score
# -------------------------------------------------

stress_scaler = MinMaxScaler()
stress_features = [
    "Work_Hours_Per_Week",
    "Overtime_Hours",
    "Projects_Handled",
    "Sick_Days"
]

df_stress_scaled = df.copy()
df_stress_scaled[stress_features] = stress_scaler.fit_transform(
    df_stress_scaled[stress_features]
)

# -------------------------------------------------
# 3️⃣ Compute Stress Score (balanced & stable)
# -------------------------------------------------

interaction = (
    df_stress_scaled["Work_Hours_Per_Week"] *
    df_stress_scaled["Overtime_Hours"]
)

stress_score = (
    0.30 * (df_stress_scaled["Work_Hours_Per_Week"] ** 1.3) +
    0.25 * (df_stress_scaled["Overtime_Hours"] ** 1.2) +
    0.20 * (1 - df_stress_scaled["Employee_Satisfaction_Score"]) +
    0.10 * interaction +
    0.10 * df_stress_scaled["Projects_Handled"] +
    0.05 * df_stress_scaled["Sick_Days"]
)

low_threshold = stress_score.quantile(0.33)
high_threshold = stress_score.quantile(0.66)

min_stress = stress_score.min()
max_stress = stress_score.max()

df["Stress_Label"] = np.where(
    stress_score < low_threshold, 0,
    np.where(stress_score < high_threshold, 1, 2)
)

# Optional check
print("Label distribution:")
print(df["Stress_Label"].value_counts())

# -------------------------------------------------
# 4️⃣ Train RandomForest Model
# -------------------------------------------------

features = [
    "Work_Hours_Per_Week",
    "Overtime_Hours",
    "Employee_Satisfaction_Score",
    "Projects_Handled",
    "Sick_Days",
    "Performance_Score"
]

X = df[features]
y = df["Stress_Label"]

model_scaler = MinMaxScaler()
X_scaled = model_scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

print("Model trained and ready")

# -------------------------------------------------
# 5️⃣ Prediction Function
# -------------------------------------------------

def predict_stress(user_data: dict):

    sample = pd.DataFrame([user_data])

    # Normalize Satisfaction & Performance (same scaler used in training)
    sample[["Employee_Satisfaction_Score", "Performance_Score"]] = \
        sat_perf_scaler.transform(
            sample[["Employee_Satisfaction_Score", "Performance_Score"]]
        )

    # ---------
    # Compute user's stress_score (scientific method)
    # ---------

    sample_stress = sample.copy()

    # Normalize workload features using stress_scaler
    sample_stress[stress_features] = stress_scaler.transform(
        sample_stress[stress_features]
    )

    interaction = (
        sample_stress["Work_Hours_Per_Week"] *
        sample_stress["Overtime_Hours"]
    )

    user_stress_score = (
        0.30 * (sample_stress["Work_Hours_Per_Week"] ** 1.3) +
        0.25 * (sample_stress["Overtime_Hours"] ** 1.2) +
        0.20 * (1 - sample_stress["Employee_Satisfaction_Score"]) +
        0.10 * interaction +
        0.10 * sample_stress["Projects_Handled"] +
        0.05 * sample_stress["Sick_Days"]
    ).values[0]

    # Convert to percentile (0–100 scale)
    stress_percentage = (
        (user_stress_score - min_stress) /
        (max_stress - min_stress)
    ) * 100

    stress_percentage = max(0, min(100, round(stress_percentage, 2)))

    # ---------
    # Predict Label using model
    # ---------

    # Keep only training features (VERY IMPORTANT)
    if stress_percentage < 33:
        stress_level = "LOW"
    elif stress_percentage < 66:
        stress_level = "MODERATE"
    else:
        stress_level = "HIGH"

    return stress_level, stress_percentage