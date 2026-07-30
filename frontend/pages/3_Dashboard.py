import streamlit as st

from utils.styles import apply_global_styles, risk_badge, COLORS
from utils.charts import create_risk_donut_chart, create_drivers_bar_chart
from utils.components import check_auth, render_footer, render_kpi_card

st.set_page_config(page_title="Executive Dashboard - TeleGuard AI", layout="wide")

apply_global_styles()
check_auth()

st.markdown('<p class="main-title">Executive Churn Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Real-time overview of customer portfolio health, churn drivers, and risk metrics.</p>',
    unsafe_allow_html=True
)

batch_result = st.session_state.get("batch_result")

if not batch_result:
    with st.container(border=True):
        st.markdown('<div class="card-title" style="font-size: 1.4rem; text-align: center;">No Active Batch Analysis Data</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-text" style="max-width: 540px; margin: 0.6rem auto 1.8rem auto; font-size: 1rem; text-align: center;">'
            'To view executive dashboard insights and risk trends, please upload and analyze a customer dataset in the Batch Analysis module.'
            '</div>',
            unsafe_allow_html=True
        )
        col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
        with col_cta2:
            if st.button("Run Batch Analysis", use_container_width=True, type="primary"):
                st.switch_page("pages/2_Batch_Analysis.py")

else:
    health = batch_result.get("company_health", {})
    drivers = batch_result.get("top_churn_drivers", [])
    action = batch_result.get("recommended_business_action", {})
    exec_summary = batch_result.get("executive_summary", "")

    total_customers = health.get("total_customers", 0)
    high_count = health.get("high_risk_count", 0)
    medium_count = health.get("medium_risk_count", 0)
    low_count = health.get("low_risk_count", 0)
    churn_rate = health.get("churn_rate", 0.0)
    churn_rate_pct = f"{round(churn_rate * 100, 1)}%"

    # KPI Header Row
    st.markdown('<p class="section-title">Portfolio Health Metrics</p>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        render_kpi_card("Total Accounts", f"{total_customers:,}", "Active Customer Base")
    with k2:
        render_kpi_card("Overall Churn Rate", churn_rate_pct, "Segment Risk Ratio", COLORS["high_risk"] if churn_rate > 0.3 else COLORS["low_risk"])
    with k3:
        render_kpi_card("High Risk", f"{high_count:,}", f"{(high_count/total_customers*100):.1f}% of portfolio" if total_customers else "", COLORS["high_risk"])
    with k4:
        render_kpi_card("Medium Risk", f"{medium_count:,}", f"{(medium_count/total_customers*100):.1f}% of portfolio" if total_customers else "", COLORS["medium_risk"])
    with k5:
        render_kpi_card("Low Risk", f"{low_count:,}", f"{(low_count/total_customers*100):.1f}% of portfolio" if total_customers else "", COLORS["low_risk"])

    st.write("")

    # Main Visual Layout
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        # Donut Breakdown
        with st.container(border=True):
            st.markdown('<div class="card-title">Risk Proportion Distribution</div>', unsafe_allow_html=True)
            fig_donut = create_risk_donut_chart(high_count, medium_count, low_count)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Executive Summary Highlight
        with st.container(border=True):
            st.markdown('<div class="card-title">Executive Summary</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="insight-text" style="color: {COLORS["text_primary"]}; line-height: 1.65;">'
                f'{exec_summary}</div>',
                unsafe_allow_html=True
            )

    with col_right:
        # Ranked Driver List with Progress Bars
        with st.container(border=True):
            st.markdown('<div class="card-title">Ranked Churn Drivers</div>', unsafe_allow_html=True)
            if not drivers:
                st.info("No major churn drivers flagged.")
            else:
                for idx, driver in enumerate(drivers, 1):
                    pct = driver.get("percentage", 0)
                    affected = driver.get("affected_customers", 0)
                    st.markdown(
                        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">'
                        f'<span style="font-weight: 700; font-size: 0.96rem; color: {COLORS["text_primary"]};">{idx}. {driver.get("title")}</span>'
                        f'<span style="font-size: 0.88rem; color: {COLORS["text_secondary"]};">{affected} accounts ({pct}%)</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.progress(min(max(pct / 100.0, 0.0), 1.0))
                    st.write("")

        # High Impact Primary Strategic Priority Executive Callout Card
        if action:
            priority = action.get("priority", "High")
            covers_count = action.get("covers_customers", 0)
            coverage_pct = action.get("coverage_percentage", 0.0)

            with st.container(border=True):
                # Header framing tag + Priority Badge
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                        <span style="font-size: 0.78rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: {COLORS['accent']};">
                            RECOMMENDED STRATEGY
                        </span>
                        {risk_badge(priority)}
                    </div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: {COLORS['text_primary']}; margin-bottom: 0.5rem; letter-spacing: -0.01em;">
                        {action.get("strategy")}
                    </div>
                    <div style="font-size: 0.96rem; color: {COLORS['text_secondary']}; line-height: 1.6; margin-bottom: 1rem;">
                        {action.get("why")}
                    </div>
                """, unsafe_allow_html=True)

                # Target Coverage Metric & Visual Progress Bar
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.3rem;">
                        <span>Target Portfolio Coverage</span>
                        <span>{covers_count} accounts ({coverage_pct:.1f}%)</span>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(min(max(coverage_pct / 100.0, 0.0), 1.0))

                # Key Action Items
                st.markdown(f"""
                    <div style="font-size: 0.82rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; color: {COLORS['text_muted']}; margin-top: 1.2rem; margin-bottom: 0.5rem;">
                        Key Action Items
                    </div>
                """, unsafe_allow_html=True)
                for act in action.get("business_action", []):
                    st.markdown(f'<div style="font-size: 0.95rem; color: {COLORS["text_secondary"]}; line-height: 1.6; margin-bottom: 0.3rem; padding-left: 0.4rem;">&bull; {act}</div>', unsafe_allow_html=True)

render_footer()
