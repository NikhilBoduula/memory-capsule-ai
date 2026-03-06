import random
import re

def generate_quiz(summary_text):

    sentences = re.split(r'[.!?]', summary_text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 40]

    questions = []

    for sentence in sentences[:5]:

        words = sentence.split()
        if len(words) < 8:
            continue

        # pick a random important word (not too short)
        important_words = [w for w in words if len(w) > 5]
        if not important_words:
            continue

        answer = random.choice(important_words)

        question_text = sentence.replace(answer, "_____")

        # generate fake options
        fake_options = random.sample(
            [w for w in words if w != answer and len(w) > 4],
            min(3, len(words)-1)
        )

        options = fake_options + [answer]
        random.shuffle(options)

        # label options A/B/C/D
        labeled_options = []
        correct_letter = None

        for idx, opt in enumerate(options):
            letter = chr(65 + idx)
            labeled_options.append(f"{letter}) {opt}")
            if opt == answer:
                correct_letter = letter

        questions.append({
            "question": question_text,
            "options": labeled_options,
            "answer": correct_letter
        })

    return questions