from app.rag.rag_engine import generate_recommendation
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"


def generate_recommendations(stress_data: dict) -> dict:
    """
    Calls local Ollama model to generate personalized recommendations
    based on stress prediction and weekly metrics.
    """
    # Retrieve relevant knowledge from RAG
    rag_context = generate_recommendation(
        user_data=stress_data,
        stress_level=stress_data.get("stress_level"),
        stress_percentage=stress_data.get("stress_percentage"),
        top_k=4
    )
    prompt = f"""
    You are a workplace wellness assistant.

    
    Use the following expert knowledge when generating advice:

    {rag_context}

    ------------------------------------
    User Profile:
    Name: {stress_data.get("name", "User")}
    Age: {stress_data.get("age", "Not specified")}
    Job Field: {stress_data.get("work_field", "Not specified")}
    Normal Sleep: {stress_data.get("normal_sleep_hours", "Not specified")} hours
    Normal Work Hours: {stress_data.get("normal_work_hours", "Not specified")} hours/day

    Current Weekly Metrics:
    Stress Level: {stress_data.get("stress_level")}
    Stress Percentage: {stress_data.get("stress_percentage")}
    Work Hours Per Week: {stress_data.get("Work_Hours_Per_Week")}
    Overtime Hours: {stress_data.get("Overtime_Hours")}
    Employee Satisfaction Score: {stress_data.get("Employee_Satisfaction_Score")}
    Projects Handled: {stress_data.get("Projects_Handled")}
    Sick Days: {stress_data.get("Sick_Days")}
    Performance Score: {stress_data.get("Performance_Score")}

    Generate:

    1. Three personalized recommendations.
    2. A 5-item weekly actionable checklist.

    Return the response in JSON format like this:

    {{
    "recommendations": ["...", "...", "..."],
    "weekly_checklist": ["...", "...", "...", "...", "..."]
    }}

    Return ONLY raw JSON.
    Do NOT use markdown.
    Do NOT wrap the output in triple backticks.
    Do NOT add explanations.
    Output must be valid JSON only.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    result = response.json()

    model_output = result.get("response", "").strip()

    # Remove markdown blocks if present
    if "```" in model_output:
        model_output = model_output.split("```")[1]

# Remove leading 'json' if model prints it
    if model_output.lower().startswith("json"):
        model_output = model_output[4:].strip()

# Attempt JSON parsing
    try:
        parsed = json.loads(model_output)
        return parsed
    except json.JSONDecodeError:
        print("⚠ JSON Parsing Failed. Raw Output:")
        print(model_output)

    return {
        "recommendations": [model_output],
        "weekly_checklist": []
    }
    