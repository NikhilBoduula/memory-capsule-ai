import re
from collections import Counter

def generate_concept_map(text):

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

    stop_words = {
        "this","that","with","from","have","will","your","about",
        "there","their","which","when","where","what","these",
        "those","been","being","into","than","them","they",
        "would","could","should","while","after","before"
    }

    filtered = [w for w in words if w not in stop_words]

    most_common = Counter(filtered).most_common(10)

    concepts = [word for word, _ in most_common]

    return concepts
