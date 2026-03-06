from transformers import pipeline

# Load once (important for performance)
summarizer = pipeline(
    task="text-generation",
    model="google/flan-t5-base"
)

def generate_summary(text):
    prompt = f"Summarize the following article clearly and concisely:\n\n{text[:1000]}"

    result = summarizer(
        prompt,
        max_length=200,
        do_sample=False
    )

    return result[0]["generated_text"]