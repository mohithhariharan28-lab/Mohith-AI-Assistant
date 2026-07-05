import streamlit as st

def get_background_html() -> str:
    """
    Returns the HTML structure for the animated space background,
    including the starry layout, shifting auroras, and fluid blobs.
    """
    return """
    <div class="space-background">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
        <div class="blob blob-4"></div>
        <div class="aurora"></div>
        <div class="stars"></div>
    </div>
    """

def inject_background():
    """
    Injects the custom HTML background element wrapper into the app.
    """
    st.markdown(get_background_html(), unsafe_allow_html=True)
