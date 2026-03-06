from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def compare_articles(text1, text2):
    emb1 = model.encode([text1[:2000]])
    emb2 = model.encode([text2[:2000]])

    similarity = cosine_similarity(emb1, emb2)[0][0]
    return round(float(similarity) * 100, 2)