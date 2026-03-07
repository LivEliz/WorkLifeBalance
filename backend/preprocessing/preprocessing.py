print("=== PREPROCESSING SCRIPT STARTED ===")

import pandas as pd
import numpy as np

df = pd.read_csv("../data/Employee_dataset.csv")

df.drop_duplicates(inplace=True)

numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

selected_features = [
    "Work_Hours_Per_Week",
    "Projects_Handled",
    "Overtime_Hours",
    "Sick_Days",
    "Employee_Satisfaction_Score",
    "Performance_Score"
]

df = df[selected_features]

df.to_csv("../data/clean_employee_data.csv", index=False)

print("=== PREPROCESSING COMPLETED ===")