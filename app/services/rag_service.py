# app/services/rag_service.py

from app.rag.rag_engine import generate_recommendation

def get_recommendations(user_data, stress_level, stress_percentage):
    recommendations = generate_recommendation(
        user_data,
        stress_level,
        stress_percentage
    )

    return recommendations