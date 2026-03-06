import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_concepts(text, top_n=10):
    doc = nlp(text)

    keywords = [
        token.text.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop
    ]

    freq = Counter(keywords)
    return freq.most_common(top_n)


def generate_concept_map(text):
    concepts = extract_concepts(text)

    concept_map = "🧩 Key Concepts:\n\n"
    for word, count in concepts:
        concept_map += f"- {word} (importance: {count})\n"

    return concept_map