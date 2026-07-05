import time
import os
import streamlit as st
import pandas as pd
import altair as alt
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Import config and other modules
import config
import prompts
import utils
from ai_client import AIClient

# Import modularized components and utilities
from visual_utils.theme import inject_theme
from visual_utils.animation import inject_background
from components.sidebar import render_sidebar
from components.cards import render_feature_card, render_kpi_dashboard, render_prompt_card
from components.chat import render_chat_workspace

# Set page configuration settings
st.set_page_config(
    page_title="Mohith AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject all visual style sheets (cached at resource level)
inject_theme()

# Inject the animated mesh and glowing blobs HTML layout
inject_background()

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state.api_key = config.OPENROUTER_API_KEY
if "model" not in st.session_state:
    st.session_state.model = config.DEFAULT_MODEL
if "temperature" not in st.session_state:
    st.session_state.temperature = config.DEFAULT_TEMPERATURE
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = config.DEFAULT_MAX_TOKENS

# Chat Workspace State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "current_feature" not in st.session_state:
    st.session_state.current_feature = "General Chat"
if "prompt_style" not in st.session_state:
    st.session_state.prompt_style = "Medium"
if "last_api_request" not in st.session_state:
    st.session_state.last_api_request = None
if "feedback_submitted" not in st.session_state:
    # Keyed by message index to track feedback status
    st.session_state.feedback_submitted = {}

# Optimize Client Initialization: Persistent Singleton in session state
if "ai_client" not in st.session_state or st.session_state.ai_client.api_key != st.session_state.api_key:
    st.session_state.ai_client = AIClient(st.session_state.api_key)

ai_client = st.session_state.ai_client

# Render Left Sidebar Panel (returns the selected page name)
selected_page = render_sidebar(ai_client)

# Page Routing
if selected_page == "Home":
    st.markdown(
        """
        <div class="hero-section">
            <div class="ai-avatar-animated">🤖</div>
            <h1 style="font-size: 3.2rem; font-weight: 800; margin-bottom: 10px; line-height: 1.2;">
                Welcome, <span class="gradient-text">Mohith</span>
            </h1>
            <p style="font-size: 1.2rem; color: #94A3B8; max-width: 800px; margin: 0 auto 30px auto; font-family: 'Poppins', sans-serif;">
                Your premium futuristic generative AI assistant workspace. Explore customized templates, prompt styles, and interactive responses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Grid of Features
    st.markdown("### 🛠️ Specialized AI Features Available")
    
    features_list = list(config.FEATURES.items())
    col1, col2 = st.columns(2)
    
    for idx, (feat_name, feat_details) in enumerate(features_list):
        col = col1 if idx % 2 == 0 else col2
        with col:
            render_feature_card(
                title=feat_name,
                description=feat_details["description"],
                icon=feat_details["icon"]
            )
            
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Quick launch button
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("💬 Launch Active Chat Workspace", use_container_width=True):
            st.info("Please select 'Chat' in the sidebar navigation menu to begin your session.")
        st.markdown("</div>", unsafe_allow_html=True)

elif selected_page == "Chat":
    # Delegate to chat module rendering
    render_chat_workspace(ai_client)

elif selected_page == "Prompt Library":
    st.markdown("# 📚 Prompt Library & Templates")
    st.markdown("Explore and study the precise system engineering templates used by Mohith AI Assistant to structure OpenRouter completions.")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    feat_selected = st.selectbox(
        "Select Feature Template",
        options=list(config.FEATURES.keys())
    )
    
    st.markdown(f"### {config.FEATURES[feat_selected]['icon']} {feat_selected} prompts")
    st.write(f"*{config.FEATURES[feat_selected]['description']}*")
    
    cols = st.columns(3)
    for idx, style in enumerate(["Concise", "Medium", "Detailed"]):
        with cols[idx]:
            sample_placeholder = prompts.USER_TEMPLATES[feat_selected]["placeholder"]
            formatter_text = prompts.USER_TEMPLATES[feat_selected]["formatter"](sample_placeholder)
            render_prompt_card(
                style=style,
                system_prompt=prompts.SYSTEM_PROMPTS[feat_selected][style],
                formatter_text=formatter_text
            )

elif selected_page == "History":
    st.markdown("# 📜 Chat Session History")
    st.markdown("Browse and inspect earlier conversations archived during your current session.")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("No saved chat sessions. Click 'New Chat' inside the Workspace to archive your active session.")
    else:
        # List of past sessions
        session_options = [
            f"[{sess['timestamp']}] Feature: {sess['feature']} ({len(sess['messages'])} messages)"
            for idx, sess in enumerate(st.session_state.history)
        ]
        
        selected_session_idx = st.selectbox(
            "Select Session to Browse",
            options=range(len(st.session_state.history)),
            format_func=lambda x: session_options[x]
        )
        
        sess_data = st.session_state.history[selected_session_idx]
        
        # Action Buttons for History
        hist_col1, hist_col2 = st.columns([1, 3])
        with hist_col1:
            if st.button("🔄 Restore to Workspace", use_container_width=True):
                st.session_state.messages = sess_data["messages"].copy()
                st.session_state.current_feature = sess_data["feature"]
                st.session_state.feedback_submitted = {}
                st.success("Session restored! Go to 'Chat' page to continue.")
                
        st.write("---")
        
        # Display archived messages as read-only blocks
        for m in sess_data["messages"]:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
                if m["role"] == "assistant":
                    st.caption(f"⏱️ Time: {m.get('response_time', 0.0):.2f}s | ✍️ Words: {m.get('word_count', 0)}")

elif selected_page == "Feedback":
    st.markdown("# 📊 Feedback Analytics Logs")
    st.markdown("Inspect user feedback submissions saved dynamically inside the local `feedback.csv` file.")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # Load from cached loader to prevent repeated disk queries
    df = utils.load_feedback_csv_cached()
    
    if df.empty:
        st.info("No feedback entries recorded in feedback.csv yet.")
    else:
        helpful_count = len(df[df["Helpful"] == "Yes"])
        total_count = len(df)
        ratio = (helpful_count / total_count * 100) if total_count > 0 else 0
        
        # Glassmorphic KPI Cards dashboard
        render_kpi_dashboard(total_count, helpful_count, ratio)
        
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        
        # Visual Analytics Charts
        st.markdown("### 📊 Interactive Metrics Dashboard")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎯 Helpful Distribution")
            helpful_counts = df["Helpful"].value_counts().reset_index()
            helpful_counts.columns = ["Helpful", "Count"]
            
            donut_chart = alt.Chart(helpful_counts).mark_arc(innerRadius=60, outerRadius=90).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Helpful", type="nominal", scale=alt.Scale(
                    domain=["Yes", "No"],
                    range=["#00E5FF", "#8B5CF6"]
                )),
                tooltip=["Helpful", "Count"]
            ).properties(
                height=220
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(donut_chart, use_container_width=True)
            
        with chart_col2:
            st.markdown("#### 📈 Response Frequency")
            df_dates = df.copy()
            df_dates["Date"] = pd.to_datetime(df_dates["Timestamp"]).dt.strftime("%Y-%m-%d")
            timeline = df_dates.groupby("Date").size().reset_index(name="Count")
            
            line_chart = alt.Chart(timeline).mark_line(
                color="#00E5FF",
                strokeWidth=3,
                point=alt.OverlayMarkDef(color="#6C63FF", size=60)
            ).encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("Count:Q", title="Total Logged"),
                tooltip=["Date:T", "Count"]
            ).properties(
                height=220
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(line_chart, use_container_width=True)
            
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("### 📋 Submission Log Details")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

elif selected_page == "Settings":
    st.markdown("# ⚙️ System Settings")
    st.markdown("Configure your credentials, model selections, and response hyper-parameters.")
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    # API Configuration Section
    st.markdown("### 🔑 API Authentication")
    
    api_key_input = st.text_input(
        "OpenRouter API Key",
        value=st.session_state.api_key if st.session_state.api_key else "",
        type="password",
        help="Input your secret OpenRouter API key. This is saved in-memory for the current session."
    )
    
    validate_col1, validate_col2 = st.columns([1, 4])
    with validate_col1:
        if st.button("🔑 Save Key", use_container_width=True):
            st.session_state.api_key = api_key_input
            # Recreate cached singleton client
            st.session_state.ai_client = AIClient(api_key_input)
            st.success("API Key updated locally!")
            st.rerun()
            
    with validate_col2:
        if st.button("🔍 Validate API Key", use_container_width=True):
            if not api_key_input:
                st.error("Please enter a key to validate.")
            else:
                with st.spinner("Validating with OpenRouter..."):
                    validator = AIClient(api_key_input)
                    if validator.validate_api_key() == "Valid":
                        st.success("API Key is VALID and working!")
                    else:
                        st.error("API Key validation failed. Please check the key and billing status.")

    st.markdown("---")
    
    # Model Configurations Section
    st.markdown("### 🎛️ Model Parameters")
    
    st.session_state.model = st.selectbox(
        "Select OpenRouter Model",
        options=list(config.AVAILABLE_MODELS.keys()),
        format_func=lambda x: config.AVAILABLE_MODELS[x],
        index=list(config.AVAILABLE_MODELS.keys()).index(st.session_state.model)
    )
    
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Higher values make output more creative and random; lower values make it more deterministic."
    )
    
    st.session_state.max_tokens = st.slider(
        "Max Generation Tokens",
        min_value=50,
        max_value=4096,
        value=st.session_state.max_tokens,
        step=50,
        help="The maximum number of tokens to generate in the completion response."
    )
    
    st.markdown("---")
    
    # Reset Defaults Button
    if st.button("🔄 Reset Configuration to System Defaults"):
        st.session_state.model = config.DEFAULT_MODEL
        st.session_state.temperature = config.DEFAULT_TEMPERATURE
        st.session_state.max_tokens = config.DEFAULT_MAX_TOKENS
        st.success("Reset settings successfully!")
        st.rerun()

elif selected_page == "About":
    st.markdown("# 🤖 About Mohith AI Assistant")
    st.markdown(
        "**Mohith AI Assistant** is a professional workspace engineered to explore prompt design and "
        "deliver specialized generative solutions. Using distinct prompts optimized for Concise, Medium, and Detailed layouts, "
        "users can draft resumes, analyze text, generate code solutions, structure business concepts, and much more."
    )
    
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Technology Stack Specifications")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Framework", "Streamlit")
    with cols[1]:
        st.metric("Language", "Python 3")
    with cols[2]:
        st.metric("Language Model API", "OpenRouter Chat")
    with cols[3]:
        st.metric("Feedback Database", "pandas & CSV")
        
    st.markdown("### ⚙️ How Prompt Engineering Styles Work")
    st.write(
        "Each AI Tool in this workspace uses a custom-tailored *System Prompt* combined with the user's formatted input: \n\n"
        "- **Concise:** Designed to produce direct, action-oriented content under 150 words. Perfect for rapid summaries or quick bullet reviews.\n"
        "- **Medium:** Standard format delivering informative outlines with bulleted points and summary explanations. Suitable for standard tasks.\n"
        "- **Detailed:** In-depth researcher model instructing the engine to produce detailed descriptions, analogies, step-by-step guides, and caveats."
    )