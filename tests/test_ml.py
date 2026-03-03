from models.ml_model import predict_stress

user_input = {
    "Work_Hours_Per_Week": 60,
    "Overtime_Hours": 20,
    "Employee_Satisfaction_Score": 2,
    "Projects_Handled": 12,
    "Sick_Days": 3,
    "Performance_Score": 2
}

level, percent = predict_stress(user_input)

print("Stress Level:", level)
print("Stress %:", percent)