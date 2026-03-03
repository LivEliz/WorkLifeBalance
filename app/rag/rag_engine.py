"""
Optimized RAG Engine
Personalized FAISS Retrieval
"""

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("=== RAG ENGINE INITIALIZING ===")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KB_PATH = os.path.join(BASE_DIR, "knowledge_base", "stress_tips.json")
VECTOR_DIR = os.path.join(BASE_DIR, "vector_store")
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
METADATA_PATH = os.path.join(VECTOR_DIR, "metadata.npy")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

os.makedirs(VECTOR_DIR, exist_ok=True)

# -------------------------
# Load embedding model once
# -------------------------
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# -------------------------
# Build or Load Vector Store
# -------------------------
def build_vector_store():
    print("Building FAISS index...")

    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = [item["content"] for item in data]

    embeddings = model.encode(documents)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)
    np.save(METADATA_PATH, data)

    return index, data


def load_vector_store():
    print("Loading existing FAISS index...")
    index = faiss.read_index(INDEX_PATH)
    metadata = np.load(METADATA_PATH, allow_pickle=True)
    return index, metadata


# -------------------------
# Initialize Index
# -------------------------
if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
    index, metadata = load_vector_store()
else:
    index, metadata = build_vector_store()

print("=== RAG ENGINE READY ===")


# -------------------------
# Personalized Retrieval
# -------------------------
def generate_recommendation(user_data, stress_level, stress_percentage, top_k=4):
    """
    Personalized semantic retrieval using full user profile
    """

    query = f"""
    Stress level: {stress_level}
    Stress percentile: {stress_percentage}
    Work hours per week: {user_data.get('Work_Hours_Per_Week')}
    Overtime hours: {user_data.get('Overtime_Hours')}
    Satisfaction score: {user_data.get('Employee_Satisfaction_Score')}
    Performance score: {user_data.get('Performance_Score')}
    Projects handled: {user_data.get('Projects_Handled')}
    Sick days: {user_data.get('Sick_Days')}
    Sleep hours: {user_data.get('Sleep_Hours', 'unknown')}
    Family time: {user_data.get('Family_Time', 'unknown')}
    Exercise hours: {user_data.get('Exercise_Hours', 'unknown')}
    """

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    retrieved = []

    for i in indices[0]:
        chunk = metadata[i]
        retrieved.append(chunk["content"])

    return "\n\n".join(retrieved)