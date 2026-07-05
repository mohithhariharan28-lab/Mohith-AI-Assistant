import os
import streamlit as st

@st.cache_resource
def load_stylesheet_content(filename: str) -> str:
    """
    Reads a stylesheet file from assets/ and caches its content 
    to maximize performance and eliminate disk queries on successive runs.
    """
    # Adjust path because this file is in utils/
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    filepath = os.path.join(assets_dir, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"/* Error loading {filename}: {e} */"
    return f"/* {filename} not found */"

def inject_theme():
    """
    Injects all cached visual stylesheets into the Streamlit session.
    """
    background_css = load_stylesheet_content("background.css")
    animations_css = load_stylesheet_content("animations.css")
    styles_css = load_stylesheet_content("styles.css")
    
    combined_css = f"{background_css}\n{animations_css}\n{styles_css}"
    st.markdown(f"<style>{combined_css}</style>", unsafe_allow_html=True)
