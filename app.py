import streamlit as st
from extractor import extract_text_from_url
from summarizer import generate_summary
from quiz_generator import generate_quiz
from tts_engine import generate_audio
from concept_mapper import generate_concept_map
from semantic_search import create_embeddings, get_relevant_chunks
from article_comparison import compare_articles
from streamlit_lottie import st_lottie
import validators
import requests
import json

# =========================================================
# 🔹 PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="🧠 Memory Capsule AI",
    layout="wide",
    page_icon="🧠"
)

# =========================================================
# 🔹 LOAD LOTTIE
# =========================================================

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_loading = load_lottie_url(
    "https://assets2.lottiefiles.com/packages/lf20_usmfx6bp.json"
)

# =========================================================
# 🔹 HERO SECTION
# =========================================================

st.markdown("""
<h1 style='text-align:center;'>🧠 Memory Capsule AI</h1>
<p style='text-align:center; font-size:18px;'>
Turn Any Article Into Summary • Quiz • Concept Map • AI Podcast • Compare Articles
</p>
<hr>
""", unsafe_allow_html=True)

# =========================================================
# 🔹 ARTICLE ANALYSIS
# =========================================================

st.markdown("## 🔎 Analyze Single Article")
url = st.text_input("🔗 Paste Article URL")

if st.button("✨ Analyze Article"):

    if not validators.url(url):
        st.error("⚠ Please enter a valid URL.")
    else:
        try:
            loading_placeholder = st.empty()

            with loading_placeholder.container():
                st_lottie(lottie_loading, height=200)
                st.markdown("### 🤖 AI is analyzing your article...")
                progress_bar = st.progress(0)

            # Extract text
            text = extract_text_from_url(url)
            st.session_state["article_text"] = text
            progress_bar.progress(20)

            # Create embeddings ONCE
            chunks, embeddings = create_embeddings(text)
            st.session_state["chunks"] = chunks
            st.session_state["embeddings"] = embeddings
            progress_bar.progress(40)

            # Generate outputs
            summary = generate_summary(text)
            quiz = generate_quiz(summary)
            concepts = generate_concept_map(text)
            audio_file = generate_audio(summary)
            audio_bytes = open(audio_file, "rb").read()

            # Store everything in session state
            st.session_state["summary"] = summary
            st.session_state["quiz"] = quiz
            st.session_state["concepts"] = concepts
            st.session_state["audio"] = audio_bytes
            st.session_state["word_count"] = len(text.split())
            st.session_state["reading_time"] = round(len(text.split()) / 200)

            progress_bar.progress(100)
            loading_placeholder.empty()

        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================
# 🔹 DISPLAY RESULTS (Stable Section)
# =========================================================

if "summary" in st.session_state:

    col1, col2 = st.columns(2)
    col1.metric("📊 Word Count", st.session_state["word_count"])
    col2.metric("⏱ Estimated Reading Time (mins)", st.session_state["reading_time"])

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Summary", "📝 Quiz", "🧠 Concepts", "🎧 Podcast"]
    )

    # ---------------- SUMMARY ----------------
    with tab1:
        st.success(st.session_state["summary"])

    # ---------------- QUIZ ----------------
    with tab2:

        st.subheader("📝 Interactive Quiz")

        quiz = st.session_state["quiz"]

        if isinstance(quiz, list) and len(quiz) > 0:

            score = 0

            for i, q in enumerate(quiz):

                st.write(f"### Q{i+1}. {q['question']}")

                user_answer = st.radio(
                    "Choose one:",
                    q["options"],
                    key=f"question_{i}"
                )

                if user_answer.startswith(q["answer"]):
                    score += 1

            if st.button("Submit Quiz"):

                total = len(quiz)
                percentage = (score / total) * 100

                st.success(f"Your Score: {score}/{total}")
                st.metric("Score Percentage", f"{round(percentage,2)} %")
                st.progress(int(percentage))

                if percentage >= 80:
                    st.success("🏆 Expert Level!")
                elif percentage >= 50:
                    st.warning("⚡ Intermediate Level")
                else:
                    st.info("📘 Beginner Level — Revise Again!")

        else:
            st.error("Quiz could not be generated properly.")

    # ---------------- CONCEPTS ----------------
    with tab3:
        st.write(st.session_state["concepts"])

    # ---------------- PODCAST ----------------
    with tab4:
        st.audio(st.session_state["audio"], format="audio/mp3")

# =========================================================
# 🔹 SEMANTIC SEARCH (RAG)
# =========================================================

if "chunks" in st.session_state and "embeddings" in st.session_state:

    st.markdown("---")
    st.markdown("## 🔍 Ask About This Article")

    user_question = st.text_input("Ask a question about the article")

    if user_question:

        top_chunks, confidence = get_relevant_chunks(
            st.session_state["chunks"],
            st.session_state["embeddings"],
            user_question
        )

        context_text = "\n\n".join(top_chunks)

        answer = generate_summary(
            f"""
            Answer the question using ONLY the context below.
            If the answer is not found, say: Not found in article.

            Context:
            {context_text}

            Question:
            {user_question}
            """
        )

        st.markdown("### 🤖 AI Answer:")
        st.success(answer)

        st.metric("Confidence Score", f"{round(confidence * 100, 2)} %")

        with st.expander("📄 Retrieved Context"):
            st.write(context_text)

# =========================================================
# 🔹 ARTICLE COMPARISON
# =========================================================

st.markdown("---")
st.markdown("## 🆚 Compare Two Articles")

col1, col2 = st.columns(2)

with col1:
    url1 = st.text_input("🔗 First Article URL")

with col2:
    url2 = st.text_input("🔗 Second Article URL")

if st.button("🔍 Compare Articles"):

    if not validators.url(url1) or not validators.url(url2):
        st.error("⚠ Please enter valid URLs for both articles.")
    else:
        try:
            with st.spinner("Analyzing similarity between articles..."):
                text1 = extract_text_from_url(url1)
                text2 = extract_text_from_url(url2)

                score = compare_articles(text1, text2)

                st.metric(
                    "📊 Similarity Score (%)",
                    f"{round(score, 2)} %"
                )

                if score > 75:
                    st.success("🔥 These articles are highly similar!")
                elif score > 40:
                    st.warning("⚡ Moderate similarity detected.")
                else:
                    st.info("🧠 Articles are mostly different.")

        except Exception as e:
            st.error(f"Error comparing articles: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + NLP + AI")