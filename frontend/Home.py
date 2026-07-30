import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.styles import apply_global_styles, COLORS
from utils.components import check_auth, render_footer

st.set_page_config(
    page_title="TeleGuard AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_styles()

# Authentication Gate
check_auth()

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown('<p class="main-title">TeleGuard AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">AI-Powered Telecom Customer Churn Prediction & Business Intelligence System</p>',
    unsafe_allow_html=True
)

st.write("")

# ---------------------------------------------------------
# Hero Section
# ---------------------------------------------------------

st.markdown("""
    <div class="hero-card">
        <h2 style="font-size: 1.8rem; font-weight: 800; color: #1b2232; margin-bottom: 0.8rem; letter-spacing: -0.02em;">
            Predict Customer Churn Before It Happens
        </h2>
        <p style="font-size: 1.05rem; color: #3D485E; max-width: 900px; line-height: 1.65; margin-bottom: 1.6rem;">
            TeleGuard AI combines XGBoost Machine Learning and Explainable AI (SHAP) to accurately predict
            which customers are likely to leave, uncover key churn drivers, and generate targeted business strategies
            to maximize customer retention.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("Predict Customer", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Predict_Customer.py")
with col2:
    if st.button("Batch Analysis", use_container_width=True):
        st.switch_page("pages/2_Batch_Analysis.py")

st.write("")

# ---------------------------------------------------------
# About Section
# ---------------------------------------------------------

st.markdown('<p class="section-title">About TeleGuard AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="body-text">'
    "TeleGuard AI is an enterprise customer churn intelligence platform built specifically for telecom operators. "
    "By combining machine learning predictive scoring with SHAP explainability, the platform enables telecom teams "
    "to proactively mitigate customer churn, protect recurring revenue, and implement targeted retention campaigns.</p>",
    unsafe_allow_html=True
)

st.write("")

# ---------------------------------------------------------
# Key Features Cards
# ---------------------------------------------------------

st.markdown('<p class="section-title">Key Capabilities</p>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
        <div class="tg-card">
            <div class="card-title">Single Customer Prediction</div>
            <div class="card-text">
                Analyze individual customer profiles in real time, generate churn probabilities, and inspect specific
                SHAP-driven risk factors with tailored retention actions.
            </div>
        </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
        <div class="tg-card">
            <div class="card-title">Batch Customer Analysis</div>
            <div class="card-text">
                Upload CSV datasets to evaluate churn risk across entire customer segments, generating company health metrics,
                risk distributions, and cohort churn drivers.
            </div>
        </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
        <div class="tg-card">
            <div class="card-title">Business Recommendations</div>
            <div class="card-text">
                Convert predictive model outputs into actionable business strategies, including contract incentives,
                promotional plans, and proactive support interventions.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# Why TeleGuard AI (Platform Benefits)
# ---------------------------------------------------------

st.markdown('<p class="section-title">Platform Benefits</p>', unsafe_allow_html=True)

b1, b2, b3, b4 = st.columns(4)

benefits = [
    ("Predictive Precision", "High-accuracy XGBoost models tailored to telecom customer telemetry data."),
    ("Transparent AI", "Explainable AI (SHAP) reveals the precise factors driving each churn score."),
    ("Business Actionability", "Directly bridges risk predictions to targeted retention strategies."),
    ("Scalable Analytics", "Seamlessly handles real-time single evaluations or large batch datasets.")
]

for col, (title, text) in zip([b1, b2, b3, b4], benefits):
    with col:
        st.markdown(f"""
            <div class="tg-card">
                <div class="card-title" style="font-size: 1.05rem;">{title}</div>
                <div class="card-text">{text}</div>
            </div>
        """, unsafe_allow_html=True)

# Footer
render_footer()