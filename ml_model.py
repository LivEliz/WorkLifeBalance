print("=== ML MODEL SCRIPT STARTED ===")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Libraries imported successfully")

# Load preprocessed dataset
df = pd.read_csv("preprocessed_employee_data.csv")
print("Preprocessed dataset loaded")
print("Shape:", df.shape)

# -------------------------------
# Create Target Variable
# -------------------------------
# Stress / Work-life imbalance logic
# 1 = Imbalanced (High stress)
# 0 = Balanced (Healthy)

df["Stress_Label"] = np.where(
    (df["Work_Hours_Per_Week"] > 0.5) &
    (df["Overtime_Hours"] > 0.5) &
    (df["Employee_Satisfaction_Score"] < 0.5),
    1,
    0
)

print("Target variable (Stress_Label) created")

# Feature set and target
X = df.drop("Stress_Label", axis=1)
y = df["Stress_Label"]

print("Features and target separated")

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train-test split completed")

# -------------------------------
# Train Random Forest Model
# -------------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
print("Random Forest model trained")

# -------------------------------
# Model Evaluation
# -------------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------
# Save Model
# -------------------------------
joblib.dump(model, "stress_prediction_model.pkl")
print("Trained model saved as stress_prediction_model.pkl")

print("=== ML MODEL SCRIPT COMPLETED ===")
