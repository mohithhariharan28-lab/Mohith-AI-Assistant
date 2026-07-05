import time
import streamlit as st
import config
from components.cards import render_profile_card

def render_sidebar(ai_client) -> str:
    """
    Renders the left navigation sidebar and returns the selected page name.
    Includes active indicator highlights and status boxes.
    """
    with st.sidebar:
        # Branding logo
        st.markdown(
            """
            <div class="sidebar-logo">
                <h1 class="gradient-text" style="font-size: 2.2rem; margin-bottom: 2px; letter-spacing: -1px;">🤖 Mohith AI</h1>
                <div style="background: rgba(0, 229, 255, 0.1); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 20px; display: inline-block; padding: 2px 12px; font-size: 0.75rem; color: #00E5FF; font-weight: 600;">
                    ⚡ OpenRouter Workspace
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # New Chat action
        st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
        if st.button("➕ New Chat Session", key="sidebar_new_chat_btn", use_container_width=True):
            if len(st.session_state.messages) > 0:
                session_summary = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "feature": st.session_state.current_feature,
                    "messages": st.session_state.messages.copy()
                }
                st.session_state.history.append(session_summary)
            st.session_state.messages = []
            st.session_state.feedback_submitted = {}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        
        # Page selection Radio (styled by CSS)
        selected_page = st.radio(
            "Navigation Menu",
            options=config.SIDEBAR_OPTIONS,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        
        # API Connection
        st.markdown("### ⚡ API Status")
        if ai_client.is_configured():
            st.success("API Key is Configured")
        else:
            st.warning("API Key Missing (Setup in Settings)")

        # User profile box at bottom (now shows OpenRouter badge via cards module)
        render_profile_card()
        
    return selected_page
