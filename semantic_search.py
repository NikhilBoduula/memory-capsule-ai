from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=250):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def create_embeddings(text):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)
    return chunks, embeddings

def get_relevant_chunks(chunks, embeddings, query, top_k=3):

    query_embedding = model.encode([query])

    similarities = cosine_similarity(query_embedding, embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    top_chunks = [chunks[i] for i in top_indices]
    confidence = float(np.max(similarities))

    return top_chunks, confidence