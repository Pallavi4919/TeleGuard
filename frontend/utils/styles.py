import streamlit as st

# ---------------------------------------------------------
# Color Palette - Telecom Light Theme
# ---------------------------------------------------------

COLORS = {
    "background": "#fffbfc",
    "card_background": "#dce1e7",
    "card_hover": "#d0d7e1",
    "sidebar_background": "#1b2232",
    "text_primary": "#1b2232",
    "text_secondary": "#3D485E",
    "text_muted": "#5C687D",
    "accent": "#4a78a6",
    "accent_hover": "#3A628C",
    "high_risk": "#EF4444",
    "medium_risk": "#F59E0B",
    "low_risk": "#10B981",
    "border": "rgba(74, 120, 166, 0.22)",
    "border_strong": "#BCC5D0"
}


# ---------------------------------------------------------
# Global CSS Injection
# ---------------------------------------------------------

def apply_global_styles():
    st.markdown(f"""
        <style>
            /* Keyframe Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(8px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            /* Base App & Page Background */
            .stApp {{
                background-color: {COLORS['background']} !important;
                color: {COLORS['text_primary']} !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }}

            /* Sidebar Styling - Dark Navy Background with High Contrast Light Text */
            [data-testid="stSidebar"] {{
                background-color: {COLORS['sidebar_background']} !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            }}
            
            /* Sidebar Text Rules (Excluding Buttons) */
            [data-testid="stSidebar"] p, 
            [data-testid="stSidebar"] label, 
            [data-testid="stSidebar"] strong,
            [data-testid="stSidebar"] a {{
                color: #fffbfc !important;
            }}
            
            /* Navigation Links inside Sidebar */
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] a [data-testid="stMarkdownContainer"] p {{
                color: #dce1e7 !important;
                font-weight: 500 !important;
            }}
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover [data-testid="stMarkdownContainer"] p {{
                color: #FFFFFF !important;
            }}
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] [data-testid="stMarkdownContainer"] p {{
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }}
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: {COLORS['accent']} !important;
                border-radius: 8px !important;
            }}

            /* Sidebar Button Styling Fix - Explicit High Contrast White Text */
            [data-testid="stSidebar"] .stButton > button {{
                background-color: {COLORS['accent']} !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
            }}
            [data-testid="stSidebar"] .stButton > button *,
            [data-testid="stSidebar"] .stButton > button p,
            [data-testid="stSidebar"] .stButton > button span,
            [data-testid="stSidebar"] .stButton > button div {{
                color: #FFFFFF !important;
            }}
            [data-testid="stSidebar"] .stButton > button:hover {{
                background-color: {COLORS['accent_hover']} !important;
                color: #FFFFFF !important;
            }}

            /* General Typography Overrides */
            p, span, label, div, li, td, th {{
                color: {COLORS['text_secondary']};
            }}

            h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
                color: {COLORS['text_primary']} !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
            }}

            /* Main Page Header & Subtitles */
            .main-title {{
                font-size: 2.5rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                color: {COLORS['text_primary']};
                margin-bottom: 0.3rem;
            }}
            .subtitle {{
                font-size: 1.1rem;
                color: {COLORS['text_secondary']};
                margin-bottom: 2rem;
                font-weight: 400;
                line-height: 1.5;
            }}
            .section-title {{
                font-size: 1.45rem;
                font-weight: 700;
                color: {COLORS['text_primary']};
                margin-top: 2.2rem;
                margin-bottom: 1.2rem;
                letter-spacing: -0.01em;
            }}
            .body-text {{
                font-size: 1.02rem;
                color: {COLORS['text_secondary']};
                line-height: 1.65;
            }}

            /* Native Streamlit Container Border Styling (Fixes Empty Container Gaps) */
            [data-testid="stVerticalBlockBorderWrapper"] {{
                background-color: {COLORS['card_background']} !important;
                border: 1px solid {COLORS['border']} !important;
                border-radius: 14px !important;
                padding: 1.2rem !important;
                box-shadow: 0 4px 16px rgba(27, 34, 50, 0.05) !important;
                transition: all 0.2s ease-in-out !important;
                margin-bottom: 1.2rem !important;
            }}
            [data-testid="stVerticalBlockBorderWrapper"]:hover {{
                border-color: {COLORS['accent']} !important;
                box-shadow: 0 8px 24px rgba(74, 120, 166, 0.18) !important;
            }}

            /* Hero Card Container */
            .hero-card {{
                background: linear-gradient(135deg, #dce1e7 0%, #edf1f5 100%);
                border: 1px solid rgba(74, 120, 166, 0.3);
                border-radius: 16px;
                padding: 2.5rem 2rem;
                margin-bottom: 2.5rem;
                box-shadow: 0 8px 24px rgba(27, 34, 50, 0.06);
                animation: fadeIn 0.4s ease-out;
            }}

            /* Custom Enterprise Cards */
            .tg-card {{
                background-color: {COLORS['card_background']};
                border: 1px solid {COLORS['border']};
                border-radius: 14px;
                padding: 1.6rem;
                margin-bottom: 1.4rem;
                box-shadow: 0 4px 16px rgba(27, 34, 50, 0.05);
                transition: all 0.2s ease-in-out;
                animation: fadeIn 0.35s ease-out;
            }}
            .tg-card:hover {{
                border-color: {COLORS['accent']};
                box-shadow: 0 8px 24px rgba(74, 120, 166, 0.18);
                transform: translateY(-2px);
            }}

            .card-title {{
                font-size: 1.18rem;
                font-weight: 700;
                color: {COLORS['text_primary']};
                margin-bottom: 0.6rem;
            }}
            .card-text {{
                font-size: 0.95rem;
                color: {COLORS['text_secondary']};
                line-height: 1.6;
            }}

            /* KPI Cards */
            .kpi-container {{
                background-color: #FFFFFF;
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 1.1rem 1.3rem;
                text-align: left;
                box-shadow: 0 2px 10px rgba(27, 34, 50, 0.04);
                transition: all 0.2s ease-in-out;
            }}
            .kpi-container:hover {{
                border-color: {COLORS['accent']};
                transform: translateY(-2px);
                box-shadow: 0 6px 18px rgba(74, 120, 166, 0.15);
            }}
            .kpi-label {{
                font-size: 0.82rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: {COLORS['text_muted']};
                margin-bottom: 0.4rem;
            }}
            .kpi-value {{
                font-size: 2rem;
                font-weight: 800;
                color: {COLORS['text_primary']};
                letter-spacing: -0.02em;
                line-height: 1.2;
            }}
            .kpi-subtext {{
                font-size: 0.88rem;
                color: {COLORS['text_secondary']};
                margin-top: 0.4rem;
            }}

            /* Risk Badges */
            .risk-badge {{
                display: inline-block;
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.03em;
                text-transform: uppercase;
            }}
            .risk-high {{
                background-color: rgba(239, 68, 68, 0.12);
                color: #DC2626;
                border: 1px solid rgba(239, 68, 68, 0.35);
            }}
            .risk-medium {{
                background-color: rgba(245, 158, 11, 0.12);
                color: #D97706;
                border: 1px solid rgba(245, 158, 11, 0.35);
            }}
            .risk-low {{
                background-color: rgba(16, 185, 129, 0.12);
                color: #059669;
                border: 1px solid rgba(16, 185, 129, 0.35);
            }}

            /* Insight Row */
            .insight-row {{
                border-left: 3px solid {COLORS['accent']};
                padding-left: 1.1rem;
                margin-bottom: 1.3rem;
            }}
            .insight-driver {{
                font-size: 1.08rem;
                font-weight: 700;
                color: {COLORS['text_primary']};
                margin-bottom: 0.3rem;
            }}
            .insight-label {{
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
                color: {COLORS['text_muted']};
                margin-top: 0.5rem;
            }}
            .insight-text {{
                font-size: 0.96rem;
                color: {COLORS['text_secondary']};
                line-height: 1.6;
            }}

            /* Form Widgets Restyling (Clean Light Surfaces) */
            div[data-baseweb="select"] > div {{
                background-color: #FFFFFF !important;
                border: 1px solid {COLORS['border_strong']} !important;
                color: {COLORS['text_primary']} !important;
                border-radius: 10px !important;
            }}
            div[data-baseweb="select"] * {{
                color: {COLORS['text_primary']} !important;
            }}
            div[data-baseweb="popover"] {{
                background-color: #FFFFFF !important;
                border: 1px solid {COLORS['border_strong']} !important;
            }}
            ul[role="listbox"] {{
                background-color: #FFFFFF !important;
            }}
            li[role="option"] {{
                background-color: #FFFFFF !important;
                color: {COLORS['text_primary']} !important;
            }}
            li[role="option"]:hover {{
                background-color: rgba(74, 120, 166, 0.15) !important;
            }}

            /* Input Fields */
            input[type="text"], input[type="password"], input[type="number"], .stNumberInput input {{
                background-color: #FFFFFF !important;
                border: 1px solid {COLORS['border_strong']} !important;
                color: {COLORS['text_primary']} !important;
                border-radius: 10px !important;
            }}
            input:focus, .stNumberInput input:focus {{
                border-color: {COLORS['accent']} !important;
                box-shadow: 0 0 0 2px rgba(74, 120, 166, 0.25) !important;
            }}

            /* File Uploader Container */
            [data-testid="stFileUploader"] {{
                background-color: #FFFFFF !important;
                border: 1px dashed {COLORS['border_strong']} !important;
                border-radius: 12px !important;
                padding: 1.2rem !important;
            }}
            [data-testid="stFileUploader"] section {{
                background-color: #FFFFFF !important;
            }}
            [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {{
                color: {COLORS['text_secondary']} !important;
            }}

            /* Dataframe / Tables */
            [data-testid="stDataFrame"] {{
                background-color: #FFFFFF !important;
                border: 1px solid {COLORS['border']} !important;
                border-radius: 12px !important;
            }}
            [data-testid="stDataFrame"] * {{
                color: {COLORS['text_primary']} !important;
            }}

            /* Main Page Buttons */
            .stMainBlockContainer .stButton > button {{
                border-radius: 10px !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
                padding: 0.6rem 1.4rem !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                border: 1px solid {COLORS['accent']} !important;
                background-color: #FFFFFF !important;
                color: {COLORS['accent']} !important;
            }}
            .stMainBlockContainer .stButton > button:hover {{
                background-color: {COLORS['card_background']} !important;
                border-color: {COLORS['accent_hover']} !important;
                color: {COLORS['accent_hover']} !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 18px rgba(74, 120, 166, 0.2) !important;
            }}
            .stMainBlockContainer .stButton > button[kind="primary"] {{
                background-color: {COLORS['accent']} !important;
                border-color: {COLORS['accent']} !important;
                color: #FFFFFF !important;
                box-shadow: 0 4px 14px rgba(74, 120, 166, 0.3) !important;
            }}
            .stMainBlockContainer .stButton > button[kind="primary"]:hover {{
                background-color: {COLORS['accent_hover']} !important;
                border-color: {COLORS['accent_hover']} !important;
                color: #FFFFFF !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 22px rgba(74, 120, 166, 0.4) !important;
            }}

            /* Tabs Styling */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: transparent !important;
                gap: 1rem !important;
                border-bottom: 1px solid {COLORS['border']} !important;
            }}
            .stTabs [data-baseweb="tab"] {{
                background-color: transparent !important;
                color: {COLORS['text_muted']} !important;
                font-weight: 600 !important;
                padding: 0.6rem 1rem !important;
            }}
            .stTabs [aria-selected="true"] {{
                color: {COLORS['text_primary']} !important;
                border-bottom: 2px solid {COLORS['accent']} !important;
            }}

            /* Dark Navy Accent Footer */
            .footer-container {{
                background-color: {COLORS['sidebar_background']};
                border-radius: 14px;
                margin-top: 4rem;
                padding: 2rem 1.5rem;
                text-align: center;
                color: #dce1e7;
                font-size: 0.88rem;
                line-height: 1.7;
            }}
            .footer-brand {{
                font-weight: 700;
                color: #FFFFFF;
            }}
        </style>
    """, unsafe_allow_html=True)


def risk_badge(risk_level: str) -> str:
    level_lower = risk_level.lower()
    if "high" in level_lower:
        css_class = "risk-high"
    elif "medium" in level_lower:
        css_class = "risk-medium"
    else:
        css_class = "risk-low"
    return f'<span class="risk-badge {css_class}">{risk_level} Risk</span>'