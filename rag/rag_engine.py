"""
RAG ENGINE
----------
Retrieval-Augmented Generation module for
Work-Life Balance & Stress Management System
"""

print("=== RAG ENGINE STARTED ===")

# =========================
# Imports
# =========================
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

print("Libraries imported successfully")

# =========================
# Configuration
# =========================
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base", "stress_tips.txt")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# =========================
# Utility Functions
# =========================
def load_knowledge_base(file_path):
    """Load stress management documents grouped by category"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Knowledge base not found at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split into sections using blank lines
    sections = content.split("\n\n")

    # Remove empty sections
    documents = [section.strip() for section in sections if section.strip()]

    return documents



def create_embeddings(documents, model):
    """Convert documents to vector embeddings"""
    return model.encode(documents)


def build_faiss_index(embeddings):
    """Build FAISS index for similarity search"""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def retrieve_relevant_docs(query, model, index, documents, top_k=2):
    """Retrieve most relevant documents for a query"""
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return [documents[i] for i in indices[0]]


# =========================
# Main RAG Logic
# =========================
def generate_recommendation(stress_level):
    documents = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    print("Knowledge base loaded")

    # Direct section filtering (more reliable)
    for doc in documents:
        if f"[{stress_level.upper()}]" in doc:
            return [doc]

    # Fallback to semantic retrieval (if no direct match)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    doc_embeddings = create_embeddings(documents, model)
    print("Document embeddings created")

    index = build_faiss_index(np.array(doc_embeddings))
    print("FAISS index created")

    query = f"Stress management tips for {stress_level}"
    relevant_docs = retrieve_relevant_docs(query, model, index, documents)

    return relevant_docs




# =========================
# Execution
# =========================
if __name__ == "__main__":
    # Take stress level as input argument
    import sys

    if len(sys.argv) > 1:
        stress_level = sys.argv[1]
    else:
        print("Please provide stress level (Low / Medium / High)")
        sys.exit()

    recommendations = generate_recommendation(stress_level)

    print(f"\nBased on your stress level ({stress_level}), here are some suggestions:\n")

    for rec in recommendations:
        cleaned = rec.replace(f"[{stress_level.upper()}]", "").strip()
        print(cleaned)

print("=== RAG ENGINE COMPLETED ===")


