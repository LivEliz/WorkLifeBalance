print("=== ML MODEL SCRIPT STARTED ===")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
import joblib
import subprocess

print("Libraries imported successfully")


# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = pd.read_csv("../data/preprocessed_employee_data.csv")
print("Dataset loaded")
print("Shape:", df.shape)


# -------------------------------------------------
# Normalize selected features for stress scoring
# -------------------------------------------------
scaler_temp = MinMaxScaler()

cols_to_normalize = [
    "Work_Hours_Per_Week",
    "Overtime_Hours",
    "Projects_Handled",
    "Sick_Days"
]

df[cols_to_normalize] = scaler_temp.fit_transform(df[cols_to_normalize])


# -------------------------------------------------
# Nonlinear Stress Score + Interaction Effect
# -------------------------------------------------
interaction = df["Work_Hours_Per_Week"] * df["Overtime_Hours"]

stress_score = (
    0.30 * (df["Work_Hours_Per_Week"] ** 1.3) +
    0.25 * (df["Overtime_Hours"] ** 1.2) +
    0.20 * (1 - df["Employee_Satisfaction_Score"]) +
    0.10 * interaction +
    0.10 * df["Projects_Handled"] +
    0.05 * df["Sick_Days"]
)


# -------------------------------------------------
# Dynamic Percentile-Based Labels
# -------------------------------------------------
low_threshold = stress_score.quantile(0.33)
high_threshold = stress_score.quantile(0.66)

df["Stress_Label"] = np.where(
    stress_score < low_threshold, 0,
    np.where(stress_score < high_threshold, 1, 2)
)

print("Stress labels created using percentile thresholds")
print(df["Stress_Label"].value_counts())


# -------------------------------------------------
# Features
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


# -------------------------------------------------
# Scale Features for Training
# -------------------------------------------------
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)


# -------------------------------------------------
# Train-Test Split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)


# -------------------------------------------------
# Train Random Forest
# -------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42
)

model.fit(X_train, y_train)
print("Model trained successfully")


# -------------------------------------------------
# Evaluation
# -------------------------------------------------
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Low", "Moderate", "High"]
))


# -------------------------------------------------
# Feature Importance
# -------------------------------------------------
importance = pd.Series(model.feature_importances_, index=features)
print("\nFeature Importance:\n")
print(importance.sort_values(ascending=False))


# -------------------------------------------------
# Save Model + Scaler
# -------------------------------------------------
joblib.dump(model, "stress_prediction_model.pkl")
joblib.dump(scaler, "stress_scaler.pkl")

print("Model and scaler saved successfully")


# -------------------------------------------------
# Real-Time Prediction + RAG Integration
# -------------------------------------------------
def predict_stress():
    print("\n=== Enter Employee Details (RAW values) ===")

    work = float(input("Work hours per week: "))
    overtime = float(input("Overtime hours: "))
    satisfaction = float(input("Satisfaction score (0-1): "))
    projects = float(input("Projects handled: "))
    sick = float(input("Sick days: "))
    performance = float(input("Performance score (0-1): "))

    sample = pd.DataFrame([{
        "Work_Hours_Per_Week": work,
        "Overtime_Hours": overtime,
        "Employee_Satisfaction_Score": satisfaction,
        "Projects_Handled": projects,
        "Sick_Days": sick,
        "Performance_Score": performance
    }])

    # Scale using trained scaler
    sample_scaled = scaler.transform(sample)

    pred = model.predict(sample_scaled)[0]
    prob = model.predict_proba(sample_scaled)[0]

    label_map = {
        0: "LOW",
        1: "MODERATE",
        2: "HIGH"
    }

    predicted_label = label_map[pred]

    print("\nPredicted Stress Level:", predicted_label)
    print("\nPrediction Confidence:")
    print(f"Low: {prob[0]*100:.2f}%")
    print(f"Moderate: {prob[1]*100:.2f}%")
    print(f"High: {prob[2]*100:.2f}%")

    # -------------------------------------------------
    # Call RAG Engine
    # -------------------------------------------------
    print("\n=== FETCHING RECOMMENDATIONS FROM RAG ===\n")

    subprocess.run([
        "python",
        "../rag/rag_engine.py",
        predicted_label
    ])


predict_stress()

print("=== ML MODEL SCRIPT COMPLETED ===")

