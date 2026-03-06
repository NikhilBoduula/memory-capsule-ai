import spacy

# Load spaCy model safely
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def generate_concept_map(text):
    doc = nlp(text)

    concepts = set()

    # Extract named entities
    for ent in doc.ents:
        concepts.add(ent.text)

    # Extract important nouns
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 3:
            concepts.add(token.text)

    return list(concepts)
