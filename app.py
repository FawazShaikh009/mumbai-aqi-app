"""
India AQI Predictor — Premium Dark Dashboard
Stunning glassmorphism UI with animated elements and persistent sidebar.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India AQI Predictor",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;600&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg-base:     #060910;
    --bg-panel:    #0c1118;
    --bg-card:     #101720;
    --bg-elevated: #141e2a;
    --border:      #1a2535;
    --border-bright: #243040;
    --text-primary: #eef2f8;
    --text-secondary: #7a90ad;
    --text-muted:  #3d5068;
    --accent:      #3b82f6;
    --accent-glow: rgba(59,130,246,0.2);
    --good:        #22d35e;
    --moderate:    #f5c842;
    --poor:        #f97316;
    --verypoor:    #ef4444;
    --severe:      #a855f7;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
}

/* ── Dark base ── */
.stApp {
    background: var(--bg-base);
}

/* Animated gradient background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 10% 0%, rgba(59,130,246,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 90% 100%, rgba(168,85,247,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(34,211,94,0.02) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1020 0%, #080d18 100%) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.4);
}

/* Fix sidebar collapse/expand button always visible */
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 8px !important;
    color: var(--accent) !important;
}
button[kind="headerNoPadding"],
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 0 8px 8px 0 !important;
    color: var(--accent) !important;
    position: fixed !important;
    left: 0 !important;
    top: 50% !important;
    z-index: 9999 !important;
    padding: 12px 6px !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-secondary) !important;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--accent) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 8px !important;
    margin-top: 20px !important;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    padding: 16px 20px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(37,99,235,0.4), inset 0 1px 0 rgba(255,255,255,0.1) !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 36px rgba(37,99,235,0.6), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Gauge cards ── */
.gauge-wrap {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-elevated));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 8px 8px 0;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.gauge-wrap::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, transparent 60%);
    pointer-events: none;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-elevated));
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 20px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.3s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.04;
}
.metric-card.good::before   { background: linear-gradient(90deg, #22d35e, #16a34a); }
.metric-card.good::after    { background: #22d35e; }
.metric-card.moderate::before { background: linear-gradient(90deg, #f5c842, #ca8a04); }
.metric-card.moderate::after  { background: #f5c842; }
.metric-card.poor::before   { background: linear-gradient(90deg, #f97316, #c2410c); }
.metric-card.poor::after    { background: #f97316; }
.metric-card.verypoor::before { background: linear-gradient(90deg, #ef4444, #b91c1c); }
.metric-card.verypoor::after  { background: #ef4444; }
.metric-card.severe::before { background: linear-gradient(90deg, #a855f7, #7c3aed); }
.metric-card.severe::after  { background: #a855f7; }

.metric-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3rem;
    font-weight: 600;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: -0.02em;
}
.metric-value.good     { color: var(--good); text-shadow: 0 0 30px rgba(34,211,94,0.3); }
.metric-value.moderate { color: var(--moderate); text-shadow: 0 0 30px rgba(245,200,66,0.3); }
.metric-value.poor     { color: var(--poor); text-shadow: 0 0 30px rgba(249,115,22,0.3); }
.metric-value.verypoor { color: var(--verypoor); text-shadow: 0 0 30px rgba(239,68,68,0.3); }
.metric-value.severe   { color: var(--severe); text-shadow: 0 0 30px rgba(168,85,247,0.3); }

.metric-delta {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.02em;
}
.metric-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-good     { background: rgba(34,211,94,0.1);  color: var(--good);     border: 1px solid rgba(34,211,94,0.25); }
.badge-moderate { background: rgba(245,200,66,0.1); color: var(--moderate); border: 1px solid rgba(245,200,66,0.25); }
.badge-poor     { background: rgba(249,115,22,0.1); color: var(--poor);     border: 1px solid rgba(249,115,22,0.25); }
.badge-verypoor { background: rgba(239,68,68,0.1);  color: var(--verypoor); border: 1px solid rgba(239,68,68,0.25); }
.badge-severe   { background: rgba(168,85,247,0.1); color: var(--severe);   border: 1px solid rgba(168,85,247,0.25); }

/* ── Section titles ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 32px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-bright), transparent);
}

/* ── Page header ── */
.page-header {
    padding: 8px 0 24px;
    position: relative;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 6px;
}
.page-title span {
    background: linear-gradient(135deg, #60a5fa, #3b82f6, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.page-subtitle {
    color: var(--text-secondary);
    font-size: 0.92rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.city-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(99,102,241,0.08));
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
    padding: 6px 18px;
    border-radius: 24px;
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin: 16px 0 24px;
}

/* ── Advisory cards ── */
.advisory-card {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-elevated));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
}
.advisory-title {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.advisory-text {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* ── Alert banners ── */
.warning-banner {
    background: linear-gradient(135deg, rgba(239,68,68,0.06), rgba(239,68,68,0.02));
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 3px solid var(--verypoor);
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 20px;
    color: #fca5a5;
    font-size: 0.9rem;
    line-height: 1.6;
}
.safe-banner {
    background: linear-gradient(135deg, rgba(34,211,94,0.06), rgba(34,211,94,0.02));
    border: 1px solid rgba(34,211,94,0.2);
    border-left: 3px solid var(--good);
    border-radius: 12px;
    padding: 18px 22px;
    margin-top: 20px;
    color: #86efac;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── AQI scale bar ── */
.aqi-scale-wrap {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
}
.aqi-scale {
    display: flex;
    border-radius: 6px;
    overflow: hidden;
    height: 10px;
    margin: 10px 0;
    gap: 2px;
}
.scale-good     { flex: 1; background: var(--good);     border-radius: 4px 0 0 4px; }
.scale-moderate { flex: 1; background: var(--moderate); }
.scale-poor     { flex: 1; background: var(--poor); }
.scale-verypoor { flex: 1; background: var(--verypoor); }
.scale-severe   { flex: 1; background: var(--severe);   border-radius: 0 4px 4px 0; }
.scale-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-top: 8px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Stats row ── */
.stat-pill {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.stat-pill-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.stat-pill-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
}

/* ── Sidebar brand ── */
.sidebar-brand {
    padding: 12px 4px 8px;
}
.sidebar-brand-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    color: var(--text-primary) !important;
    letter-spacing: 0.04em;
}
.sidebar-brand-sub {
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    margin-top: 2px;
}

/* ── Welcome screen ── */
.welcome-box {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-elevated));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 48px 40px;
    text-align: center;
    margin-top: 24px;
    position: relative;
    overflow: hidden;
}
.welcome-box::before {
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.welcome-icon { font-size: 3.5rem; margin-bottom: 18px; filter: drop-shadow(0 0 20px rgba(59,130,246,0.3)); }
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
}
.welcome-text { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7; }

/* ── City grid ── */
.city-chip {
    font-size: 0.76rem;
    color: var(--text-secondary);
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    padding: 5px 10px;
    border-radius: 6px;
    text-align: center;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; }

/* ── Hide streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CITIES = sorted([
    'Agartala', 'Ahmedabad', 'Aizawl', 'Bengaluru', 'Bhopal',
    'Bhubaneswar', 'Chandigarh', 'Chennai', 'Dehradun', 'Delhi',
    'Gangtok', 'Gurugram', 'Guwahati', 'Hyderabad', 'Imphal',
    'Itanagar', 'Jaipur', 'Kohima', 'Kolkata', 'Lucknow',
    'Mumbai', 'Panaji', 'Patna', 'Raipur', 'Ranchi',
    'Shillong', 'Shimla', 'Thiruvananthapuram', 'Visakhapatnam'
])

CITY_STATES = {
    'Agartala': 'Tripura', 'Ahmedabad': 'Gujarat', 'Aizawl': 'Mizoram',
    'Bengaluru': 'Karnataka', 'Bhopal': 'Madhya Pradesh',
    'Bhubaneswar': 'Odisha', 'Chandigarh': 'Chandigarh',
    'Chennai': 'Tamil Nadu', 'Dehradun': 'Uttarakhand', 'Delhi': 'Delhi',
    'Gangtok': 'Sikkim', 'Gurugram': 'Haryana', 'Guwahati': 'Assam',
    'Hyderabad': 'Telangana', 'Imphal': 'Manipur', 'Itanagar': 'Arunachal Pradesh',
    'Jaipur': 'Rajasthan', 'Kohima': 'Nagaland', 'Kolkata': 'West Bengal',
    'Lucknow': 'Uttar Pradesh', 'Mumbai': 'Maharashtra', 'Panaji': 'Goa',
    'Patna': 'Bihar', 'Raipur': 'Chhattisgarh', 'Ranchi': 'Jharkhand',
    'Shillong': 'Meghalaya', 'Shimla': 'Himachal Pradesh',
    'Thiruvananthapuram': 'Kerala', 'Visakhapatnam': 'Andhra Pradesh'
}

AQI_INFO = {
    "Good":      {"color": "#22d35e", "css": "good",     "icon": "✅", "advice": "Air quality is satisfactory. Great day for outdoor activities and exercise!"},
    "Moderate":  {"color": "#f5c842", "css": "moderate", "icon": "🟡", "advice": "Acceptable air quality. Sensitive individuals should limit prolonged outdoor exertion."},
    "Poor":      {"color": "#f97316", "css": "poor",     "icon": "😷", "advice": "Unhealthy for sensitive groups. Reduce prolonged outdoor exertion."},
    "Very Poor": {"color": "#ef4444", "css": "verypoor", "icon": "🚨", "advice": "Unhealthy for everyone. Avoid prolonged outdoor activity. Keep windows closed."},
    "Severe":    {"color": "#a855f7", "css": "severe",   "icon": "☠️",  "advice": "Hazardous! Stay indoors. Wear N95 mask if going out is absolutely unavoidable."},
}

def get_risk(aqi):
    if aqi <= 50:    return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 200: return "Poor"
    elif aqi <= 300: return "Very Poor"
    else:            return "Severe"

def make_gauge(aqi, label, color):
    # Convert hex color to rgba for steps (Plotly requires valid color strings)
    step_colors = {
        "#22d35e": "rgba(34, 211, 94, 0.07)",
        "#f5c842": "rgba(245, 200, 66, 0.07)",
        "#f97316": "rgba(249, 115, 22, 0.07)",
        "#ef4444": "rgba(239, 68, 68, 0.07)",
        "#a855f7": "rgba(168, 85, 247, 0.07)",
    }
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={
            'text': label,
            'font': {'size': 12, 'color': '#3d5068', 'family': 'Outfit'}
        },
        number={
            'font': {'size': 42, 'color': color, 'family': 'JetBrains Mono'},
            'suffix': ''
        },
        gauge={
            'axis': {
                'range': [0, 400],
                'tickwidth': 1,
                'tickcolor': '#1a2535',
                'tickfont': {'color': '#3d5068', 'size': 9, 'family': 'JetBrains Mono'},
                'nticks': 5
            },
            'bar': {'color': color, 'thickness': 0.22},
            'bgcolor': '#0c1118',
            'borderwidth': 0,
            'steps': [
                {'range': [0,   50],  'color': 'rgba(34, 211, 94, 0.07)'},
                {'range': [50,  100], 'color': 'rgba(245, 200, 66, 0.07)'},
                {'range': [100, 200], 'color': 'rgba(249, 115, 22, 0.07)'},
                {'range': [200, 300], 'color': 'rgba(239, 68, 68, 0.07)'},
                {'range': [300, 400], 'color': 'rgba(168, 85, 247, 0.07)'},
            ],
            'threshold': {
                'line': {'color': color, 'width': 2},
                'thickness': 0.75,
                'value': aqi
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=24, r=24, t=36, b=8),
        height=210,
        font={'family': 'Outfit'}
    )
    return fig

def make_trend_chart(current_aqi, aqi_24, aqi_48, info_now, info_24, info_48):
    fig = go.Figure()

    # Background shading zones
    zones = [
        (0, 50, 'rgba(34,211,94,0.03)'),
        (50, 100, 'rgba(245,200,66,0.03)'),
        (100, 200, 'rgba(249,115,22,0.03)'),
        (200, 300, 'rgba(239,68,68,0.03)'),
        (300, 400, 'rgba(168,85,247,0.03)'),
    ]
    for y0, y1, color in zones:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0)

    max_val = max(current_aqi, aqi_24, aqi_48)

    # Bars
    fig.add_trace(go.Bar(
        x=["Now", "24h Forecast", "48h Forecast"],
        y=[current_aqi, aqi_24, aqi_48],
        marker=dict(
            color=[info_now['color'], info_24['color'], info_48['color']],
            opacity=0.9,
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[str(current_aqi), str(aqi_24), str(aqi_48)],
        textposition='outside',
        textfont=dict(color='#eef2f8', family='JetBrains Mono', size=14),
        width=0.35
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=240,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='#7a90ad', family='Outfit', size=12),
            showline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#1a2535',
            gridwidth=1,
            tickfont=dict(color='#3d5068', family='JetBrains Mono', size=10),
            range=[0, max_val * 1.35],
            showline=False,
            zeroline=False,
        ),
        showlegend=False,
        bargap=0.5,
    )
    return fig

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model    = joblib.load("india_aqi_model_streamlit.pkl")
    features = joblib.load("india_model_features.pkl")
    return model, features

try:
    model, FEATURES = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🌫️ AQI PREDICTOR</div>
        <div class="sidebar-brand-sub">India · 29 Cities · 24h & 48h Forecast</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📍 Location")
    city = st.selectbox("City", CITIES, index=CITIES.index("Mumbai"), label_visibility="collapsed")
    state = CITY_STATES[city]
    st.markdown(f'<div style="font-size:0.78rem;color:#3b82f6;margin:-6px 0 10px 2px;font-family:Outfit,sans-serif;">📌 {state}</div>', unsafe_allow_html=True)

    st.markdown("### 🌤️ Weather Conditions")
    c1, c2 = st.columns(2)
    with c1:
        temp     = st.number_input("Temp (°C)",    -5.0, 50.0,  28.0, 0.5)
        humidity = st.number_input("Humidity (%)",  0,   100,   65)
        wind_spd = st.number_input("Wind (km/h)",   0.0, 100.0, 12.0, 0.5)
    with c2:
        pressure = st.number_input("Pressure (hPa)", 950.0, 1050.0, 1010.0, 0.5)
        dew_pt   = st.number_input("Dew Pt (°C)",   -10.0, 40.0,   20.0,   0.5)
        precip   = st.number_input("Rain (mm)",      0.0,  200.0,   0.0,   0.5)
    wind_dir = st.slider("Wind Direction (°)", 0, 360, 180)

    st.markdown("### 💨 Pollutant Levels")
    c3, c4 = st.columns(2)
    with c3:
        pm25 = st.number_input("PM2.5",  0.0, 500.0,  35.0, 1.0)
        pm10 = st.number_input("PM10",   0.0, 600.0,  55.0, 1.0)
        no2  = st.number_input("NO₂",    0.0, 200.0,  20.0, 1.0)
    with c4:
        o3   = st.number_input("O₃",     0.0, 300.0,  40.0, 1.0)
        so2  = st.number_input("SO₂",    0.0, 100.0,   8.0, 0.5)
        co   = st.number_input("CO",     0.0,10000.0, 200.0,10.0)
    current_aqi = st.number_input("Current AQI", 0, 500, 80)

    st.markdown("### 📅 Date & Time")
    c5, c6 = st.columns(2)
    with c5:
        month  = st.selectbox("Month", range(1,13), index=10,
                               format_func=lambda m: ['Jan','Feb','Mar','Apr','May','Jun',
                                                       'Jul','Aug','Sep','Oct','Nov','Dec'][m-1])
        season = st.selectbox("Season", ["Winter","Summer","Monsoon","Post_Monsoon"])
    with c6:
        hour   = st.slider("Hour", 0, 23, 12)
        is_weekend = st.checkbox("Weekend")

    festival     = st.checkbox("🎆 Festival Period")
    crop_burning = st.checkbox("🌾 Crop Burning Season")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⬡  PREDICT AQI", use_container_width=True)

# ── Main panel ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-title">India <span>AQI</span> Predictor</div>
    <div class="page-subtitle">AI-powered 24h & 48h air quality forecast for 29 Indian cities</div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model files not found! Place `india_aqi_model_streamlit.pkl` and `india_model_features.pkl` in the same folder as `app.py`.")
    st.stop()

if predict_btn:
    # ── Build input ──────────────────────────────────────────────────────────
    input_data = {f: 0 for f in FEATURES}

    numeric_map = {
        'Temp_2m_C': temp, 'Humidity_Percent': humidity,
        'Wind_Speed_10m_kmh': wind_spd, 'Wind_Dir_10m': wind_dir,
        'Pressure_MSL_hPa': pressure, 'Surface_Pressure_hPa': pressure - 1.5,
        'Dew_Point_C': dew_pt, 'Precipitation_mm': precip, 'Rain_mm': precip,
        'PM2_5_ugm3': pm25, 'PM10_ugm3': pm10, 'PM_Ratio': pm25 / max(pm10, 1),
        'NO2_ugm3': no2, 'O3_ugm3': o3, 'SO2_ugm3': so2, 'CO_ugm3': co,
        'US_AQI': current_aqi, 'Month': month, 'Hour': hour,
        'Is_Weekend': int(is_weekend), 'Festival_Period': int(festival),
        'Crop_Burning_Season': int(crop_burning),
        'Is_Raining': int(precip > 0), 'Heavy_Rain': int(precip > 20),
    }
    for k, v in numeric_map.items():
        if k in input_data:
            input_data[k] = v

    lag_bases = ['US_AQI','PM2_5_ugm3','PM10_ugm3','NO2_ugm3','O3_ugm3',
                 'Temp_2m_C','Humidity_Percent','Wind_Speed_10m_kmh']
    lag_vals  = [current_aqi, pm25, pm10, no2, o3, temp, humidity, wind_spd]
    for base, val in zip(lag_bases, lag_vals):
        for lag in [1,3,6,12,24]:
            k = f'{base}_lag{lag}'
            if k in input_data: input_data[k] = val

    ref_city = CITIES[0]
    if city != ref_city:
        k = f'City_{city}'
        if k in input_data: input_data[k] = 1

    all_states = sorted(set(CITY_STATES.values()))
    if state != all_states[0]:
        k = f'State_{state}'
        if k in input_data: input_data[k] = 1

    for s in ["Post_Monsoon","Summer","Winter"]:
        k = f'Season_{s}'
        if k in input_data: input_data[k] = int(season == s)

    tod = ('Morning' if 6<=hour<12 else 'Afternoon' if 12<=hour<18
           else 'Evening' if 18<=hour<22 else 'Night')
    k = f'Time_of_Day_{tod}'
    if k in input_data: input_data[k] = 1

    hcat = ('Dry' if humidity<40 else 'Normal' if humidity<60
            else 'Humid' if humidity<80 else 'Very_Humid')
    k = f'Humidity_Category_{hcat}'
    if k in input_data: input_data[k] = 1

    wcat = ('Calm' if wind_spd<5 else 'Light' if wind_spd<15
            else 'Moderate' if wind_spd<30 else 'Strong')
    k = f'Wind_Category_{wcat}'
    if k in input_data: input_data[k] = 1

    X_in = pd.DataFrame([input_data])[FEATURES]
    pred = model.predict(X_in)[0]
    aqi_24 = max(0, round(pred[0]))
    aqi_48 = max(0, round(pred[1]))

    risk_now = get_risk(current_aqi)
    risk_24  = get_risk(aqi_24)
    risk_48  = get_risk(aqi_48)

    info_now = AQI_INFO[risk_now]
    info_24  = AQI_INFO[risk_24]
    info_48  = AQI_INFO[risk_48]

    # ── City tag ──────────────────────────────────────────────────────────────
    st.markdown(f'<div class="city-tag">📍 {city}, {state}</div>', unsafe_allow_html=True)

    # ── Quick stats row ───────────────────────────────────────────────────────
    s1, s2, s3, s4, s5 = st.columns(5)
    stats = [
        ("PM2.5", f"{pm25} µg/m³"),
        ("PM10",  f"{pm10} µg/m³"),
        ("NO₂",   f"{no2} µg/m³"),
        ("O₃",    f"{o3} µg/m³"),
        ("Temp",  f"{temp}°C"),
    ]
    for col, (lbl, val) in zip([s1,s2,s3,s4,s5], stats):
        col.markdown(f"""
        <div class="stat-pill">
            <div class="stat-pill-label">{lbl}</div>
            <div class="stat-pill-value">{val}</div>
        </div>""", unsafe_allow_html=True)

    # ── Gauge charts ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">AQI Forecast</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(current_aqi, "Current AQI", info_now["color"]),
                        use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(aqi_24, "24-Hour Forecast", info_24["color"]),
                        use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g3:
        st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(aqi_48, "48-Hour Forecast", info_48["color"]),
                        use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Status cards ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    delta_24 = aqi_24 - current_aqi
    delta_48 = aqi_48 - current_aqi
    arrow_24 = "↑" if delta_24 > 0 else "↓" if delta_24 < 0 else "→"
    arrow_48 = "↑" if delta_48 > 0 else "↓" if delta_48 < 0 else "→"

    with d1:
        st.markdown(f"""
        <div class="metric-card {info_now['css']}">
            <div class="metric-label">Right Now</div>
            <div class="metric-value {info_now['css']}">{current_aqi}</div>
            <div class="metric-delta">&nbsp;</div>
            <span class="metric-badge badge-{info_now['css']}">{info_now['icon']} {risk_now}</span>
        </div>""", unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="metric-card {info_24['css']}">
            <div class="metric-label">In 24 Hours</div>
            <div class="metric-value {info_24['css']}">{aqi_24}</div>
            <div class="metric-delta">{arrow_24} {abs(delta_24):+d} from now</div>
            <span class="metric-badge badge-{info_24['css']}">{info_24['icon']} {risk_24}</span>
        </div>""", unsafe_allow_html=True)

    with d3:
        st.markdown(f"""
        <div class="metric-card {info_48['css']}">
            <div class="metric-label">In 48 Hours</div>
            <div class="metric-value {info_48['css']}">{aqi_48}</div>
            <div class="metric-delta">{arrow_48} {abs(delta_48):+d} from now</div>
            <span class="metric-badge badge-{info_48['css']}">{info_48['icon']} {risk_48}</span>
        </div>""", unsafe_allow_html=True)

    # ── Trend + Advisory side by side ─────────────────────────────────────────
    st.markdown('<div class="section-title">Trend & Advisory</div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        fig_bar = make_trend_chart(current_aqi, aqi_24, aqi_48, info_now, info_24, info_48)
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with right:
        st.markdown(f"""
        <div class="advisory-card" style="border-left: 3px solid {info_24['color']}; margin-bottom: 12px;">
            <div class="advisory-title">24-Hour Advisory</div>
            <div class="advisory-text">{info_24['icon']} {info_24['advice']}</div>
        </div>
        <div class="advisory-card" style="border-left: 3px solid {info_48['color']}">
            <div class="advisory-title">48-Hour Advisory</div>
            <div class="advisory-text">{info_48['icon']} {info_48['advice']}</div>
        </div>""", unsafe_allow_html=True)

    # ── AQI scale bar ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">AQI Scale Reference</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="aqi-scale-wrap">
        <div class="aqi-scale">
            <div class="scale-good"></div>
            <div class="scale-moderate"></div>
            <div class="scale-poor"></div>
            <div class="scale-verypoor"></div>
            <div class="scale-severe"></div>
        </div>
        <div class="scale-labels">
            <span>✅ Good · 0–50</span>
            <span>🟡 Moderate · 51–100</span>
            <span>😷 Poor · 101–200</span>
            <span>🚨 Very Poor · 201–300</span>
            <span>☠️ Severe · 300+</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Alert banner ──────────────────────────────────────────────────────────
    if risk_24 in ['Poor','Very Poor','Severe'] or risk_48 in ['Poor','Very Poor','Severe']:
        st.markdown(f"""
        <div class="warning-banner">
            ⚠️ <strong>Early Warning</strong> — Elevated pollution expected in <strong>{city}</strong>.<br>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;">
            24h: {risk_24} (AQI {aqi_24}) &nbsp;·&nbsp; 48h: {risk_48} (AQI {aqi_48})
            </span><br>
            <span style="font-size:0.82rem;opacity:0.75;margin-top:4px;display:block;">
            Consider limiting outdoor activities and wearing an N95 mask.
            </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="safe-banner">
            ✅ <strong>Good news!</strong> Air quality looks clean for <strong>{city}</strong> over the next 48 hours.<br>
            <span style="font-size:0.82rem;opacity:0.8;">Enjoy outdoor activities — conditions are favourable.</span>
        </div>""", unsafe_allow_html=True)

else:
    # ── Welcome screen ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon">🌫️</div>
        <div class="welcome-title">Ready to Predict</div>
        <div class="welcome-text">
            Configure your city and environmental conditions in the sidebar,<br>
            then click <strong>Predict AQI</strong> to get your personalised air quality forecast.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:32px;">AQI Scale Reference</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="aqi-scale-wrap">
        <div class="aqi-scale">
            <div class="scale-good"></div><div class="scale-moderate"></div>
            <div class="scale-poor"></div><div class="scale-verypoor"></div>
            <div class="scale-severe"></div>
        </div>
        <div class="scale-labels">
            <span>✅ Good · 0–50</span>
            <span>🟡 Moderate · 51–100</span>
            <span>😷 Poor · 101–200</span>
            <span>🚨 Very Poor · 201–300</span>
            <span>☠️ Severe · 300+</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:28px;">29 Cities Covered</div>', unsafe_allow_html=True)
    rows = [CITIES[i:i+6] for i in range(0, len(CITIES), 6)]
    for row in rows:
        cols = st.columns(6)
        for col, c in zip(cols, row):
            col.markdown(f'<div class="city-chip">{c}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
