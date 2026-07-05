import streamlit as st

def render_feature_card(title: str, description: str, icon: str):
    """
    Renders a glassmorphic dashboard card for the Welcome page.
    Includes float and slide-up animations.
    """
    st.markdown(
        f"""
        <div class="custom-card slide-up">
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

def render_kpi_dashboard(total: int, helpful: int, ratio: float):
    """
    Renders glassmorphic KPI dashboard panels for Feedback metrics.
    """
    st.markdown(
        f"""
        <div class="kpi-container slide-up">
            <div class="kpi-card">
                <div class="kpi-title">Total Submissions</div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-desc">Logged in feedback.csv</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Helpful Responses (Yes)</div>
                <div class="kpi-value">{helpful}</div>
                <div class="kpi-desc">Approved by users</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Approval Rate</div>
                <div class="kpi-value">{ratio:.1f}%</div>
                <div class="kpi-desc">Positive rating percentage</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_prompt_card(style: str, system_prompt: str, formatter_text: str):
    """
    Renders styled Prompt Library code blocks in floating glass templates.
    """
    st.markdown(
        f"""
        <div class="prompt-library-card slide-up">
            <h4 style="margin-top:0; color:#00E5FF; font-family:'Poppins', sans-serif;">🏷️ {style} Template</h4>
            <div style="font-size:0.85rem; color:#94A3B8; margin-bottom:5px; font-weight:600;">System Profile:</div>
            <pre style="background:rgba(5,8,22,0.4); border:1px solid rgba(255,255,255,0.06); padding:12px; border-radius:10px; color:#E2E8F0; white-space:pre-wrap; font-family:monospace; font-size:0.8rem; margin-bottom:15px;">{system_prompt}</pre>
            <div style="font-size:0.85rem; color:#94A3B8; margin-bottom:5px; font-weight:600;">User Format Example:</div>
            <pre style="background:rgba(5,8,22,0.4); border:1px solid rgba(255,255,255,0.06); padding:12px; border-radius:10px; color:#00E5FF; white-space:pre-wrap; font-family:monospace; font-size:0.8rem;">{formatter_text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_profile_card():
    """
    Renders the custom profile panel at the bottom of the sidebar.
    """
    st.markdown(
        """
        <div class="user-profile-box">
            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #00E5FF 0%, #6C63FF 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 0.9rem;">
                M
            </div>
            <div style="flex-grow: 1; text-align: left; padding-left: 10px;">
                <div style="font-size: 0.85rem; font-weight: 600; color: #FFFFFF; line-height: 1.2;">Mohith User</div>
                <div style="font-size: 0.7rem; color: #94A3B8; line-height: 1;">Premium Plan</div>
            </div>
            <div class="openrouter-badge">v2.5</div>
        </div>
        """,
        unsafe_allow_html=True
    )
