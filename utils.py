import os
import time
import csv
from datetime import datetime
import pandas as pd
import streamlit as st

@st.cache_resource
def get_custom_css():
    """
    Reads the styles.css file and caches it to prevent disk I/O on every rerun.
    """
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            st.error(f"Error loading styles.css: {e}")
    return ""

def inject_custom_css():
    """
    Injects custom CSS to style the Streamlit interface.
    Uses the cached CSS helper.
    """
    css_content = get_custom_css()
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def calculate_word_count(text: str) -> int:
    """Calculates the word count of a string."""
    if not text:
        return 0
    return len(text.strip().split())

def init_feedback_csv(filepath: str = "feedback.csv"):
    """Initializes the feedback.csv file with headers if it does not exist."""
    if not os.path.exists(filepath):
        headers = ["Timestamp", "Feature", "Model", "Prompt Style", "Prompt Input", "Response", "Helpful", "Comment"]
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        except Exception as e:
            st.error(f"Error initializing feedback file: {e}")

def save_feedback_to_csv(feature: str, model: str, prompt_style: str, prompt_input: str, response: str, helpful: str, comment: str, filepath: str = "feedback.csv"):
    """Appends feedback to the feedback.csv file and clears the cache."""
    init_feedback_csv(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, feature, model, prompt_style, prompt_input, response, helpful, comment]
    try:
        with open(filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        # Clear the cache for DataFrame loading to force reload with new data
        load_feedback_csv_cached.clear()
        return True
    except Exception as e:
        st.error(f"Failed to record feedback: {e}")
        return False

@st.cache_data(ttl=60)
def load_feedback_csv_cached(filepath: str = "feedback.csv") -> pd.DataFrame:
    """Loads previous feedback entries into a Pandas DataFrame with caching."""
    init_feedback_csv(filepath)
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        st.error(f"Error loading feedback logs: {e}")
        return pd.DataFrame()

def render_feature_card(title: str, description: str, icon: str):
    """HTML card generator for the Home dashboard with premium glassmorphic UI."""
    st.markdown(
        f"""
        <div class="custom-card">
            <div class="custom-card-icon-wrapper">
                <span class="custom-card-icon">{icon}</span>
            </div>
            <div class="custom-card-content">
                <div class="custom-card-title">{title}</div>
                <div class="custom-card-desc">{description}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
