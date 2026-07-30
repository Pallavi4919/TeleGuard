import io
import time
import pandas as pd
import streamlit as st

from utils.styles import apply_global_styles, risk_badge, COLORS
from utils.api import predict_batch
from utils.charts import create_risk_donut_chart, create_drivers_bar_chart
from utils.components import check_auth, render_footer, render_kpi_card, REQUIRED_COLUMNS

st.set_page_config(page_title="Batch Analysis - TeleGuard AI", layout="wide")

apply_global_styles()
check_auth()

st.markdown('<p class="main-title">Batch Customer Analysis</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Upload a CSV dataset containing customer telemetry to evaluate churn distribution, drivers, and recommendations.</p>',
    unsafe_allow_html=True
)

# Read results from session state
result = st.session_state.get("batch_result")

# =========================================================
# UPLOAD VIEW MODE (If no batch_result)
# =========================================================
if result is None:
    with st.container(border=True):
        st.markdown('<div class="card-title" style="font-size: 1.3rem;">Upload Dataset</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-text" style="margin-bottom: 1.2rem;">Select a CSV file containing customer telemetry data. '
            'The file must contain required feature columns matching the dataset schema.</div>',
            unsafe_allow_html=True
        )
        st.write("")

        uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])

        df_preview = None
        validation_ok = False

        if uploaded_file is not None:
            try:
                raw_bytes = uploaded_file.getvalue()
                df_preview = pd.read_csv(io.BytesIO(raw_bytes))
                missing_cols = [c for c in REQUIRED_COLUMNS if c not in df_preview.columns]

                if missing_cols:
                    st.error(f"Dataset is missing required columns: {', '.join(missing_cols)}")
                else:
                    validation_ok = True
                    st.success(f"Dataset validated — {len(df_preview)} rows, all required columns present.")
                    st.write("")
                    st.markdown('<div style="font-weight: 700; color: #1b2232; margin-bottom: 0.5rem;">Dataset Preview (First 5 Rows):</div>', unsafe_allow_html=True)
                    st.dataframe(df_preview.head(5), use_container_width=True)
            except Exception as e:
                st.error(f"Failed to parse uploaded CSV: {e}")

        st.write("")
        analyze_btn = st.button(
            "Analyze Dataset",
            use_container_width=True,
            type="primary",
            disabled=not validation_ok
        )

    if analyze_btn and uploaded_file is not None:
        try:
            with st.spinner("Analyzing dataset..."):
                time.sleep(0.3)
                uploaded_file.seek(0)
                batch_response = predict_batch(uploaded_file)

            st.session_state["batch_result"] = batch_response
            st.session_state["batch_source_df"] = df_preview
            st.rerun()
        except Exception as e:
            st.error(f"Batch prediction service error: {e}")

# =========================================================
# REPORT VIEW MODE (When batch_result exists)
# =========================================================
else:
    health = result.get("company_health", {})
    drivers = result.get("top_churn_drivers", [])
    action = result.get("recommended_business_action", {})
    exec_summary = result.get("executive_summary", "")

    total_customers = health.get("total_customers", 0)
    high_count = health.get("high_risk_count", 0)
    medium_count = health.get("medium_risk_count", 0)
    low_count = health.get("low_risk_count", 0)
    churn_rate = health.get("churn_rate", 0.0)
    churn_rate_pct = f"{round(churn_rate * 100, 1)}%"

    # Section A: Company Health KPI Cards
    st.markdown('<p class="section-title">Company Health Summary</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render_kpi_card("Total Customers", f"{total_customers:,}", f"Overall Churn Rate: {churn_rate_pct}")
    with k2:
        render_kpi_card("High Risk Customers", f"{high_count:,}", f"{(high_count/total_customers*100):.1f}% of base" if total_customers else "", COLORS["high_risk"])
    with k3:
        render_kpi_card("Medium Risk Customers", f"{medium_count:,}", f"{(medium_count/total_customers*100):.1f}% of base" if total_customers else "", COLORS["medium_risk"])
    with k4:
        render_kpi_card("Low Risk Customers", f"{low_count:,}", f"{(low_count/total_customers*100):.1f}% of base" if total_customers else "", COLORS["low_risk"])

    st.write("")

    # Section B & C: Risk Distribution Donut & Top Churn Drivers
    row2_left, row2_right = st.columns([1, 1.4])

    with row2_left:
        with st.container(border=True):
            st.markdown('<div class="card-title">Risk Level Breakdown</div>', unsafe_allow_html=True)
            fig_donut = create_risk_donut_chart(high_count, medium_count, low_count)
            st.plotly_chart(fig_donut, use_container_width=True)

    with row2_right:
        with st.container(border=True):
            st.markdown('<div class="card-title">Top Churn Drivers Impact</div>', unsafe_allow_html=True)
            fig_bar = create_drivers_bar_chart(drivers)
            if fig_bar:
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No significant churn drivers detected in this dataset.")

    st.write("")

    # Detailed Driver Explanation Cards
    if drivers:
        with st.container(border=True):
            st.markdown('<div class="card-title">Detailed Churn Driver Analysis</div>', unsafe_allow_html=True)
            for d in drivers:
                st.markdown(f"""
                    <div class="insight-row">
                        <div class="insight-driver">
                            {d.get("title")} &bull;
                            <span style="font-weight: 500; font-size: 0.9rem; color: {COLORS['text_secondary']};">
                                Affected Customers: {d.get("affected_customers", 0)} ({d.get("percentage", 0)}%)
                            </span>
                        </div>
                        <div class="insight-label">Root Cause</div>
                        <div class="insight-text">{d.get("reason")}</div>
                        <div class="insight-label">Recommendation</div>
                        <div class="insight-text">{d.get("recommendation")}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.write("")

    # Section D: Recommended Business Strategy Card
    if action:
        priority = action.get("priority", "High")
        with st.container(border=True):
            st.markdown('<div class="card-title">Recommended Business Strategy</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div style="margin-bottom: 0.8rem;">
                    <span style="font-size: 1.25rem; font-weight: 700; color: {COLORS['text_primary']}; margin-right: 0.8rem;">
                        {action.get("strategy")}
                    </span>
                    {risk_badge(priority)}
                </div>
                <div class="insight-label">Rationale</div>
                <div class="insight-text" style="margin-bottom: 0.8rem;">{action.get("why")}</div>
                <div class="insight-label">Target Coverage</div>
                <div class="insight-text" style="margin-bottom: 0.8rem;">
                    Covers {action.get("covers_customers", 0)} customers ({action.get("coverage_percentage", 0)}% of total cohort)
                </div>
                <div class="insight-label">Action Items</div>
            """, unsafe_allow_html=True)

            for act_item in action.get("business_action", []):
                st.markdown(f'<div class="insight-text" style="padding-left: 0.8rem;">&bull; {act_item}</div>', unsafe_allow_html=True)

    st.write("")

    # Section E: Executive Summary Block
    with st.container(border=True):
        st.markdown('<div class="card-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="insight-text" style="font-size: 1.02rem; line-height: 1.65; color: {COLORS["text_primary"]};">'
            f'{exec_summary}</div>',
            unsafe_allow_html=True
        )

    st.write("")

    # Section F & G: Action Buttons (Download & Analyze Another)
    btn_col1, btn_col2, _ = st.columns([1, 1, 1])

    with btn_col1:
        source_df = st.session_state.get("batch_source_df")
        row_results = result.get("results", [])

        if source_df is not None and len(row_results) == len(source_df):
            output_df = source_df.copy().reset_index(drop=True)
            output_df["Prediction"] = ["Churn" if r.get("prediction") == 1 else "No Churn" for r in row_results]
            output_df["Churn_Probability"] = [r.get("churn_probability") for r in row_results]
            output_df["Risk_Level"] = [r.get("risk_level") for r in row_results]
            output_df["Top_Reasons"] = ["; ".join(r.get("top_reasons", [])) for r in row_results]

            csv_bytes = output_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Results (CSV)",
                data=csv_bytes,
                file_name="teleguard_batch_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )

    with btn_col2:
        if st.button("Analyze Another Dataset", use_container_width=True, type="primary"):
            st.session_state.pop("batch_result", None)
            st.session_state.pop("batch_source_df", None)
            st.rerun()

render_footer()
