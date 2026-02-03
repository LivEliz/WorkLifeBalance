print("=== ML MODEL SCRIPT STARTED ===")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Libraries imported successfully")

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
df = pd.read_csv("preprocessed_employee_data.csv")
print("Dataset loaded")
print("Shape:", df.shape)


# -------------------------------------------------
# Create 3-Level Target Variable
# 0 = Low
# 1 = Moderate
# 2 = High
# -------------------------------------------------
conditions = [
    (df["Work_Hours_Per_Week"] < 0.3),
    (df["Work_Hours_Per_Week"].between(0.3, 0.6)),
    (df["Work_Hours_Per_Week"] > 0.6)
]

values = [0, 1, 2]

df["Stress_Label"] = np.select(conditions, values)

print("Multiclass Stress_Label created")


# -------------------------------------------------
# Features and Target
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
# Train-Test Split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train-test split completed")


# -------------------------------------------------
# Train Random Forest
# -------------------------------------------------
model = RandomForestClassifier(
    n_estimators=100,
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
# Save Model
# -------------------------------------------------
joblib.dump(model, "stress_prediction_model.pkl")
print("Model saved")


# -------------------------------------------------
# Predict from user input
# -------------------------------------------------
def predict_stress():
    print("\n=== Enter Employee Details (0–1 scaled values) ===")

    work = float(input("Work hours per week: "))
    overtime = float(input("Overtime hours: "))
    satisfaction = float(input("Satisfaction score: "))
    projects = float(input("Projects handled: "))
    sick = float(input("Sick days: "))
    performance = float(input("Performance score: "))

    sample = pd.DataFrame([{
        "Work_Hours_Per_Week": work,
        "Overtime_Hours": overtime,
        "Employee_Satisfaction_Score": satisfaction,
        "Projects_Handled": projects,
        "Sick_Days": sick,
        "Performance_Score": performance
}])

    pred = model.predict(sample)[0]

    #sample = np.array([[work, overtime, satisfaction, projects, sick, performance]])

    pred = model.predict(sample)[0]

    labels = {
        0: "LOW stress 🙂",
        1: "MODERATE stress 😐",
        2: "HIGH stress 😵"
    }

    print("\nPredicted Stress Level:", labels[pred])


predict_stress()

print("=== ML MODEL SCRIPT COMPLETED ===")
