import os
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Step 13: Read from st.secrets if on Streamlit Cloud, otherwise fall back to environment variable
OPENROUTER_API_KEY = None
try:
    if "OPENROUTER_API_KEY" in st.secrets:
        OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    pass

if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DEFAULT_MODEL = "meta-llama/llama-3.3-8b-instruct:free"

DEFAULT_TEMPERATURE = 0.7

DEFAULT_MAX_TOKENS = 2048

AVAILABLE_MODELS = {
    "meta-llama/llama-3.3-8b-instruct:free": "Llama 3.3 8B Instruct (Free)",
    "deepseek/deepseek-chat-v3-0324:free": "DeepSeek Chat V3 (Free)",
    "qwen/qwen3-235b-a22b:free": "Qwen 3 235B (Free)",
    "mistralai/mistral-small-3.2-24b-instruct:free": "Mistral Small 24B (Free)"
}

SIDEBAR_OPTIONS = [
    "Home",
    "Chat",
    "Prompt Library",
    "History",
    "Feedback",
    "Settings",
    "About"
]

# Supported Features / Specialized Tools
FEATURES = {
    "General Chat": {
        "icon": "💬",
        "description": "Engage in an open-ended, assistant-led conversation on any topic."
    },
    "Answer Questions": {
        "icon": "❓",
        "description": "Provide answers, explanations, or solutions to questions with selectable depths."
    },
    "Text Summarizer": {
        "icon": "📝",
        "description": "Condense paragraphs, articles, or transcripts into brief outlines or detailed summaries."
    },
    "Business Idea Generator": {
        "icon": "💡",
        "description": "Generate unique business models, strategies, or pitch frameworks based on simple ideas."
    },
    "Story Generator": {
        "icon": "📖",
        "description": "Draft creative short stories, narratives, or creative scripts with selectable pacing."
    },
    "Email Writer": {
        "icon": "✉️",
        "description": "Compose professional emails, follow-ups, or announcements with appropriate tone."
    },
    "Resume Helper": {
        "icon": "👔",
        "description": "Draft resume summaries, rewrite bullet points, or optimize job descriptions."
    },
    "Study Assistant": {
        "icon": "🎓",
        "description": "Summarize concepts, generate revision flashcards, or create practice quizzes."
    }
}
