import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(show_spinner=False)
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text().strip() for p in paragraphs])

        return text[:5000]  # limit text length for speed

    except Exception as e:
        return f"Error extracting text: {e}"