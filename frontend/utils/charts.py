import plotly.graph_objects as go
import plotly.express as px
from utils.styles import COLORS

# ---------------------------------------------------------
# Risk Gauge Visual (Single Prediction)
# ---------------------------------------------------------

def create_risk_gauge(churn_prob: float, risk_level: str):
    """
    Creates a horizontal gauge / indicator chart for churn probability with Low, Medium, High risk zones.
    """
    prob_pct = churn_prob * 100

    level_lower = risk_level.lower()
    if "high" in level_lower:
        bar_color = COLORS["high_risk"]
    elif "medium" in level_lower:
        bar_color = COLORS["medium_risk"]
    else:
        bar_color = COLORS["low_risk"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_pct,
        number={'suffix': "%", 'font': {'size': 38, 'color': COLORS['text_primary'], 'family': '-apple-system'}},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': COLORS['text_secondary'],
                'tickfont': {'color': COLORS['text_secondary'], 'size': 12}
            },
            'bar': {'color': bar_color, 'thickness': 0.35},
            'bgcolor': "rgba(27, 34, 50, 0.04)",
            'borderwidth': 1,
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.18)'},
                {'range': [30, 70], 'color': 'rgba(245, 158, 11, 0.18)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.18)'}
            ],
            'threshold': {
                'line': {'color': bar_color, 'width': 3},
                'thickness': 0.8,
                'value': prob_pct
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=30, b=20),
        height=220,
        font=dict(color=COLORS['text_primary'], family="-apple-system")
    )

    return fig


# ---------------------------------------------------------
# Risk Distribution Donut Chart (Batch & Dashboard)
# ---------------------------------------------------------

def create_risk_donut_chart(high_count: int, medium_count: int, low_count: int):
    """
    Creates a Plotly donut chart showing the breakdown of high, medium, and low risk customers.
    """
    labels = ["High Risk", "Medium Risk", "Low Risk"]
    values = [high_count, medium_count, low_count]
    colors = [COLORS["high_risk"], COLORS["medium_risk"], COLORS["low_risk"]]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color=COLORS['card_background'], width=2)),
        textinfo="percent+value",
        textposition="inside",
        insidetextfont=dict(color="#FFFFFF", size=13, family="-apple-system"),
        hoverinfo="label+value+percent"
    )])

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS['text_secondary'], size=12)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=40),
        height=280,
        font=dict(color=COLORS['text_primary'], family="-apple-system")
    )

    return fig


# ---------------------------------------------------------
# Top Churn Drivers Horizontal Bar Chart
# ---------------------------------------------------------

def create_drivers_bar_chart(drivers: list):
    """
    Creates a Plotly horizontal bar chart of top churn drivers sorted by percentage descending.
    """
    if not drivers:
        return None

    # Sort drivers by percentage ascending for plotly horizontal bar (bottom to top)
    sorted_drivers = sorted(drivers, key=lambda x: x.get("percentage", 0), reverse=False)

    titles = [d.get("title", "Driver") for d in sorted_drivers]
    percentages = [d.get("percentage", 0) for d in sorted_drivers]
    text_labels = [f"{p:.1f}%" for p in percentages]

    fig = go.Figure(go.Bar(
        x=percentages,
        y=titles,
        orientation='h',
        text=text_labels,
        textposition='outside',
        marker=dict(
            color=COLORS['accent'],
            line=dict(color='rgba(27, 34, 50, 0.1)', width=1)
        ),
        textfont=dict(color=COLORS['text_primary'], size=12)
    ))

    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(27, 34, 50, 0.1)',
            zeroline=False,
            title=dict(text="Affected Customers (%)", font=dict(color=COLORS['text_secondary'], size=12)),
            tickfont=dict(color=COLORS['text_secondary'], size=11),
            range=[0, max(percentages) * 1.25 if percentages else 100]
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color=COLORS['text_primary'], size=12)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=40, t=20, b=40),
        height=280,
        font=dict(color=COLORS['text_primary'], family="-apple-system")
    )

    return fig
