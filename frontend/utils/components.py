import streamlit as st
from utils.styles import COLORS

# ---------------------------------------------------------
# Dataset Options & Column Definitions
# ---------------------------------------------------------

GENDER = ["Female", "Male"]
YES_NO = ["No", "Yes"]
MULTIPLE_LINES = ["No phone service", "No", "Yes"]
INTERNET_SERVICE = ["DSL", "Fiber optic", "No"]
INTERNET_DEPENDENT = ["No internet service", "No", "Yes"]
CONTRACT = ["Month-to-month", "One year", "Two year"]
PAYMENT_METHOD = [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)"
]

REQUIRED_COLUMNS = [
    "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges", "TotalCharges"
]


# ---------------------------------------------------------
# Authentication Gate
# ---------------------------------------------------------

def check_auth():
    """
    Enforces authentication across all pages.
    If unauthenticated, renders a clean login/signup screen and halts execution.
    If authenticated, renders a logout button in the sidebar.
    """
    if "auth_status" not in st.session_state:
        st.session_state["auth_status"] = False

    if st.session_state["auth_status"]:
        with st.sidebar:
            st.write("")
            st.divider()
            user_email = st.session_state.get("auth_email", "admin@teleguard.ai")
            st.markdown(
                f"<div style='font-size: 0.88rem; color: #dce1e7; margin-bottom: 0.6rem;'>"
                f"Active Account:<br><strong style='color: #FFFFFF; font-size: 0.95rem;'>{user_email}</strong>"
                f"</div>",
                unsafe_allow_html=True
            )
            if st.button("Log out", use_container_width=True):
                st.session_state["auth_status"] = False
                st.session_state.pop("auth_email", None)
                st.rerun()
        return True

    # Render clean authentication container
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        st.markdown('<p class="main-title" style="text-align: center;">TeleGuard AI</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="subtitle" style="text-align: center; color: #3D485E;">Enterprise Customer Churn Analytics Platform</p>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="tg-card">', unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.write("")
            email = st.text_input("Work Email", value="admin@teleguard.ai", key="login_email")
            password = st.text_input("Password", type="password", value="password123", key="login_password")
            st.write("")
            if st.button("Sign In to Platform", use_container_width=True, type="primary", key="btn_login"):
                if email and password:
                    st.session_state["auth_status"] = True
                    st.session_state["auth_email"] = email
                    st.rerun()
                else:
                    st.error("Please enter both email and password.")

        with tab_signup:
            st.write("")
            company = st.text_input("Company Name", value="Telecom Corp", key="signup_company")
            signup_email = st.text_input("Work Email", value="", key="signup_email")
            signup_password = st.text_input("Password", type="password", value="", key="signup_password")
            st.write("")
            if st.button("Create Account", use_container_width=True, type="primary", key="btn_signup"):
                if company and signup_email and signup_password:
                    st.session_state["auth_status"] = True
                    st.session_state["auth_email"] = signup_email
                    st.rerun()
                else:
                    st.error("Please complete all registration fields.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# ---------------------------------------------------------
# Reusable UI Components
# ---------------------------------------------------------

def render_footer():
    """Renders the standard enterprise footer on all pages."""
    st.markdown(f"""
        <div class="footer-container">
            <span class="footer-brand">TeleGuard AI</span> &bull; Enterprise Churn Prediction System<br>
            <span style="color: #dce1e7; font-size: 0.82rem; margin-top: 0.3rem; display: inline-block;">
                Built with Python, FastAPI, Streamlit, XGBoost, SHAP, and Plotly
            </span><br>
            Copyright &copy; 2026 TeleGuard AI Inc. All rights reserved.
        </div>
    """, unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtext: str = None, color: str = None):
    """Renders a styled high-contrast KPI metric card."""
    value_color = color if color else COLORS['text_primary']
    subtext_html = f'<div class="kpi-subtext">{subtext}</div>' if subtext else ''
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-label">{title}</div>
            <div class="kpi-value" style="color: {value_color};">{value}</div>
            {subtext_html}
        </div>
    """, unsafe_allow_html=True)
