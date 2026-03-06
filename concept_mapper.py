import re
from collections import Counter

def generate_concept_map(text):

    # simple word cleaning
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

    # remove common words
    stop_words = {
        "this","that","with","from","have","will","your","about",
        "there","their","which","when","where","what","these",
        "those","been","being","into","than","them","they",
        "would","could","should","while","after","before"
    }

    filtered_words = [w for w in words if w not in stop_words]

    # count important words
    most_common = Counter(filtered_words).most_common(10)

    concepts = [word for word, count in most_common]

    return concepts
