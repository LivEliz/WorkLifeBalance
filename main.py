from models.ml_model import predict_stress
from rag.rag_engine import generate_recommendation

user_input = {
    "Work_Hours_Per_Week": 60,
    "Overtime_Hours": 20,
    "Employee_Satisfaction_Score": 3,
    "Projects_Handled": 12,
    "Sick_Days": 4,
    "Performance_Score": 3
}

# Step 1 → ML
level, percent = predict_stress(user_input)

print("Stress Level:", level)
print("Stress Percentage:", percent)

# Step 2 → RAG
recommendation = generate_recommendation(level)

print("\nRecommendations:\n")
print(recommendation)