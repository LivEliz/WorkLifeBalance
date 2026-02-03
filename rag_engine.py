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
KNOWLEDGE_BASE_PATH = "rag/knowledge_base/stress_tips.txt"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# =========================
# Utility Functions
# =========================
def load_knowledge_base(file_path):
    """Load stress management documents"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Knowledge base not found at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        documents = file.readlines()

    return [doc.strip() for doc in documents if doc.strip()]


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
    """
    Core RAG pipeline:
    Stress level → Retrieve knowledge → Generate advice
    """

    # Load knowledge base
    documents = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    print("Knowledge base loaded")

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # Create embeddings
    doc_embeddings = create_embeddings(documents, model)
    print("Document embeddings created")

    # Build FAISS index
    index = build_faiss_index(np.array(doc_embeddings))
    print("FAISS index created")

    # Query construction
    query = f"Stress management tips for {stress_level} stress level"

    # Retrieve relevant content
    relevant_docs = retrieve_relevant_docs(
        query, model, index, documents
    )

    return relevant_docs


# =========================
# Execution
# =========================
if __name__ == "__main__":
    stress_level = "High"  # Example input from ML model

    recommendations = generate_recommendation(stress_level)

    print(f"\nBased on your stress level ({stress_level}), here are some suggestions:")
    for rec in recommendations:
        print("-", rec)

print("=== RAG ENGINE COMPLETED ===")
