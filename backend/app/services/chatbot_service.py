import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def chatbot_reply(prompt):

    payload = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    result = response.json()

    return result.get("response", "")