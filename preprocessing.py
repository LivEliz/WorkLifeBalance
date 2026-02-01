print("=== PREPROCESSING SCRIPT STARTED ===")

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

print("Libraries imported successfully")

# Load dataset
df = pd.read_csv("Employee_dataset.csv")
print("Dataset loaded successfully")
print("Shape:", df.shape)

# Remove duplicates
df.drop_duplicates(inplace=True)
print("Duplicates removed")

# Handle missing values
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
print("Missing values handled")

# Select features
selected_features = [
    "Work_Hours_Per_Week",
    "Projects_Handled",
    "Overtime_Hours",
    "Sick_Days",
    "Employee_Satisfaction_Score",
    "Performance_Score"
]

df = df[selected_features]
print("Features selected")

# Min-Max normalization
minmax = MinMaxScaler()
df[["Employee_Satisfaction_Score", "Performance_Score"]] = minmax.fit_transform(
    df[["Employee_Satisfaction_Score", "Performance_Score"]]
)
print("Min-Max normalization done")

# Z-score normalization
scaler = StandardScaler()
df[["Work_Hours_Per_Week", "Projects_Handled", "Overtime_Hours", "Sick_Days"]] = scaler.fit_transform(
    df[["Work_Hours_Per_Week", "Projects_Handled", "Overtime_Hours", "Sick_Days"]]
)
print("Z-score normalization done")

# Save output
df.to_csv("preprocessed_employee_data.csv", index=False)
print("File saved as preprocessed_employee_data.csv")

print("=== PREPROCESSING SCRIPT COMPLETED ===")
