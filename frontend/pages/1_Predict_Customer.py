import streamlit as st
import time
from utils.styles import apply_global_styles, risk_badge, COLORS
from utils.api import predict_customer
from utils.charts import create_risk_gauge
from utils.components import (
    check_auth, render_footer, render_kpi_card,
    GENDER, YES_NO, MULTIPLE_LINES, INTERNET_SERVICE,
    INTERNET_DEPENDENT, CONTRACT, PAYMENT_METHOD
)

st.set_page_config(page_title="Predict Customer - TeleGuard AI", layout="wide")

apply_global_styles()
check_auth()

# Track view mode: 'form' vs 'report'
if "predict_view_mode" not in st.session_state:
    st.session_state["predict_view_mode"] = "form"

st.markdown('<p class="main-title">Predict Customer Churn</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Enter customer profile details to calculate churn probability and view AI recommendations.</p>',
    unsafe_allow_html=True
)

# =========================================================
# FORM VIEW MODE
# =========================================================
if st.session_state["predict_view_mode"] == "form":
    with st.container(border=True):
        st.markdown('<div class="card-title" style="font-size: 1.3rem;">Customer Profile Form</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-text" style="margin-bottom: 1.2rem;">Provide personal, account, service, and billing information for analysis.</div>', unsafe_allow_html=True)
        st.write("")

        # Grid Section 1: Personal Information
        st.markdown('<div style="font-weight: 700; color: #1b2232; margin-bottom: 0.6rem;">Personal Information</div>', unsafe_allow_html=True)
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            gender = st.selectbox("Gender", GENDER)
        with p2:
            senior_citizen = st.selectbox("Senior Citizen", YES_NO)
        with p3:
            partner = st.selectbox("Partner", YES_NO)
        with p4:
            dependents = st.selectbox("Dependents", YES_NO)

        st.write("")
        st.divider()

        # Grid Section 2: Account Details
        st.markdown('<div style="font-weight: 700; color: #1b2232; margin-bottom: 0.6rem;">Account Details</div>', unsafe_allow_html=True)
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12, step=1)
        with a2:
            contract = st.selectbox("Contract Type", CONTRACT)
        with a3:
            paperless_billing = st.selectbox("Paperless Billing", YES_NO)
        with a4:
            payment_method = st.selectbox("Payment Method", PAYMENT_METHOD)

        st.write("")
        st.divider()

        # Grid Section 3: Services
        st.markdown('<div style="font-weight: 700; color: #1b2232; margin-bottom: 0.6rem;">Services & Features</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            phone_service = st.selectbox("Phone Service", YES_NO)
            multiple_lines = st.selectbox("Multiple Lines", MULTIPLE_LINES)
            internet_service = st.selectbox("Internet Service", INTERNET_SERVICE)
        with s2:
            online_security = st.selectbox("Online Security", INTERNET_DEPENDENT)
            online_backup = st.selectbox("Online Backup", INTERNET_DEPENDENT)
            device_protection = st.selectbox("Device Protection", INTERNET_DEPENDENT)
        with s3:
            tech_support = st.selectbox("Tech Support", INTERNET_DEPENDENT)
            streaming_tv = st.selectbox("Streaming TV", INTERNET_DEPENDENT)
            streaming_movies = st.selectbox("Streaming Movies", INTERNET_DEPENDENT)

        st.write("")
        st.divider()

        # Grid Section 4: Billing
        st.markdown('<div style="font-weight: 700; color: #1b2232; margin-bottom: 0.6rem;">Billing Information</div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1, 1, 2])
        with b1:
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0, step=1.0)
        with b2:
            total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=840.0, step=1.0)

        st.write("")
        st.write("")
        
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            analyze_clicked = st.button("Analyze Customer", use_container_width=True, type="primary")

    if analyze_clicked:
        payload = {
            "gender": gender,
            "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges
        }

        try:
            with st.spinner("Analyzing customer profile..."):
                time.sleep(0.3)
                result = predict_customer(payload)
            st.session_state["predict_result"] = result
            st.session_state["predict_view_mode"] = "report"
            st.rerun()
        except Exception as e:
            st.error(f"Failed to communicate with prediction backend: {e}")

# =========================================================
# REPORT VIEW MODE
# =========================================================
else:
    result = st.session_state.get("predict_result", {})
    if not result:
        st.session_state["predict_view_mode"] = "form"
        st.rerun()

    prediction_val = result.get("prediction", 0)
    churn_prob = result.get("churn_probability", 0.0)
    risk_level = result.get("risk_level", "Low")
    top_reasons = result.get("top_reasons", [])

    is_churn = (prediction_val == 1)
    headline_text = "Likely to Churn" if is_churn else "Likely to Stay"
    headline_color = COLORS["high_risk"] if is_churn else COLORS["low_risk"]
    prob_pct_str = f"{round(churn_prob * 100, 1)}%"

    # Top Row: Prediction Summary
    r_col1, r_col2 = st.columns([1, 1])

    with r_col1:
        with st.container(border=True):
            st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
            st.write("")
            st.markdown(
                f'<div class="kpi-label">Assessment Result</div>'
                f'<div class="kpi-value" style="color: {headline_color}; font-size: 2.3rem;">{headline_text}</div>',
                unsafe_allow_html=True
            )
            st.write("")
            render_kpi_card("Churn Probability Score", prob_pct_str, f"Risk Classification: {risk_level}")

    with r_col2:
        with st.container(border=True):
            st.markdown('<div class="card-title">Visual Risk Meter</div>', unsafe_allow_html=True)
            fig_gauge = create_risk_gauge(churn_prob, risk_level)
            st.plotly_chart(fig_gauge, use_container_width=True)

    st.write("")

    # Middle Row: Primary Reason & Action Cards
    c_reason, c_action = st.columns(2)

    primary_reason_obj = top_reasons[0] if top_reasons else None

    with c_reason:
        with st.container(border=True):
            st.markdown('<div class="card-title">Primary Risk Factor</div>', unsafe_allow_html=True)
            if primary_reason_obj:
                st.markdown(f'<div class="insight-driver">{primary_reason_obj.get("title", "Risk Factor")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="insight-text">{primary_reason_obj.get("reason", "")}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="insight-text">No significant risk factors identified for this customer profile. '
                    'The customer displays strong account stability indicators.</div>',
                    unsafe_allow_html=True
                )

    with c_action:
        with st.container(border=True):
            st.markdown('<div class="card-title">Recommended Business Action</div>', unsafe_allow_html=True)
            if primary_reason_obj and primary_reason_obj.get("recommendation"):
                st.markdown(f'<div class="insight-driver">Action Plan</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="insight-text">{primary_reason_obj.get("recommendation")}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div class="insight-text">Maintain standard customer engagement and satisfaction monitoring. '
                    'No intervention required at this time.</div>',
                    unsafe_allow_html=True
                )

    # Secondary Reasons Table if more than 1 reason
    if len(top_reasons) > 1:
        with st.container(border=True):
            st.markdown('<div class="card-title">Secondary Contributing Risk Drivers</div>', unsafe_allow_html=True)
            for reason_item in top_reasons[1:]:
                st.markdown(f"""
                    <div class="insight-row">
                        <div class="insight-driver">{reason_item.get("title")}</div>
                        <div class="insight-text">{reason_item.get("reason")}</div>
                        <div class="insight-label">Recommendation</div>
                        <div class="insight-text">{reason_item.get("recommendation")}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.write("")
    col_reset, _ = st.columns([1, 2])
    with col_reset:
        if st.button("Analyze Another Customer", use_container_width=True, type="primary"):
            st.session_state["predict_view_mode"] = "form"
            st.rerun()

render_footer()
