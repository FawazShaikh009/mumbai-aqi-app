"""
India AQI Predictor — Redesigned Streamlit App
Beautiful dark dashboard UI with gauge charts and visual AQI indicators.
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
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1525 !important;
    border-right: 1px solid #1e2a45;
}
[data-testid="stSidebar"] * {
    color: #c8d0e0 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    color: #6b7fa3 !important;
}

/* Sidebar section headers */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #4a9eff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #1e2a45;
    padding-bottom: 6px;
    margin-top: 20px !important;
}

/* Input fields */
[data-testid="stSidebar"] input {
    background: #151d30 !important;
    border: 1px solid #1e2a45 !important;
    color: #e8eaf0 !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #151d30 !important;
    border: 1px solid #1e2a45 !important;
    color: #e8eaf0 !important;
}

/* Predict button */
.stButton > button {
    background: linear-gradient(135deg, #4a9eff 0%, #0066cc 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    font-weight: 700 !important;
    padding: 14px 20px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(74, 158, 255, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(74, 158, 255, 0.5) !important;
}

/* Metric cards */
.metric-card {
    background: #0f1525;
    border: 1px solid #1e2a45;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.metric-card.good::before   { background: #00e676; }
.metric-card.moderate::before { background: #ffee58; }
.metric-card.poor::before   { background: #ff9800; }
.metric-card.verypoor::before { background: #f44336; }
.metric-card.severe::before { background: #9c27b0; }

.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7fa3;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-value.good    { color: #00e676; }
.metric-value.moderate { color: #ffee58; }
.metric-value.poor    { color: #ff9800; }
.metric-value.verypoor { color: #f44336; }
.metric-value.severe  { color: #ce93d8; }

.metric-delta {
    font-size: 0.8rem;
    color: #6b7fa3;
    margin-bottom: 6px;
}
.metric-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-good     { background: #00e67620; color: #00e676; border: 1px solid #00e67650; }
.badge-moderate { background: #ffee5820; color: #ffee58; border: 1px solid #ffee5850; }
.badge-poor     { background: #ff980020; color: #ff9800; border: 1px solid #ff980050; }
.badge-verypoor { background: #f4433620; color: #f44336; border: 1px solid #f4433650; }
.badge-severe   { background: #9c27b020; color: #ce93d8; border: 1px solid #9c27b050; }

/* Advisory cards */
.advisory-card {
    background: #0f1525;
    border: 1px solid #1e2a45;
    border-radius: 10px;
    padding: 18px 20px;
    margin-top: 8px;
}
.advisory-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7fa3;
    margin-bottom: 8px;
}
.advisory-text {
    font-size: 0.92rem;
    color: #c8d0e0;
    line-height: 1.5;
}

/* Warning banner */
.warning-banner {
    background: linear-gradient(135deg, #1a0a0a, #1a1000);
    border: 1px solid #f4433640;
    border-left: 4px solid #f44336;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 16px;
    color: #ffcdd2;
    font-size: 0.9rem;
}
.safe-banner {
    background: linear-gradient(135deg, #0a1a0a, #0a150a);
    border: 1px solid #00e67640;
    border-left: 4px solid #00e676;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 16px;
    color: #b9f6ca;
    font-size: 0.9rem;
}

/* Page title */
.page-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #e8eaf0;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.page-subtitle {
    color: #6b7fa3;
    font-size: 0.9rem;
    margin-bottom: 24px;
}
.city-tag {
    display: inline-block;
    background: #4a9eff20;
    border: 1px solid #4a9eff40;
    color: #4a9eff;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
}
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a9eff;
    margin-bottom: 12px;
    margin-top: 28px;
    border-bottom: 1px solid #1e2a45;
    padding-bottom: 8px;
}

/* AQI scale bar */
.aqi-scale {
    display: flex;
    border-radius: 6px;
    overflow: hidden;
    height: 8px;
    margin: 12px 0;
}
.scale-good     { flex: 1; background: #00e676; }
.scale-moderate { flex: 1; background: #ffee58; }
.scale-poor     { flex: 1; background: #ff9800; }
.scale-verypoor { flex: 1; background: #f44336; }
.scale-severe   { flex: 1; background: #9c27b0; }

/* Divider */
.custom-divider {
    border: none;
    border-top: 1px solid #1e2a45;
    margin: 24px 0;
}

/* Welcome screen */
.welcome-box {
    background: #0f1525;
    border: 1px solid #1e2a45;
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    margin-top: 40px;
}
.welcome-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}
.welcome-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.2rem;
    color: #e8eaf0;
    margin-bottom: 8px;
}
.welcome-text {
    color: #6b7fa3;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
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
    "Good":      {"color": "#00e676", "css": "good",     "icon": "✅", "advice": "Air quality is satisfactory. Great day for outdoor activities!"},
    "Moderate":  {"color": "#ffee58", "css": "moderate", "icon": "🟡", "advice": "Acceptable air quality. Sensitive individuals should limit prolonged outdoor exertion."},
    "Poor":      {"color": "#ff9800", "css": "poor",     "icon": "😷", "advice": "Unhealthy for sensitive groups. Reduce prolonged outdoor exertion."},
    "Very Poor": {"color": "#f44336", "css": "verypoor", "icon": "🚨", "advice": "Unhealthy for everyone. Avoid prolonged outdoor activity."},
    "Severe":    {"color": "#ce93d8", "css": "severe",   "icon": "☠️", "advice": "Hazardous! Stay indoors. Wear N95 mask if going out is unavoidable."},
}

def get_risk(aqi):
    if aqi <= 50:    return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 200: return "Poor"
    elif aqi <= 300: return "Very Poor"
    else:            return "Severe"

def make_gauge(aqi, label, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': label, 'font': {'size': 13, 'color': '#6b7fa3', 'family': 'DM Sans'}},
        number={'font': {'size': 36, 'color': color, 'family': 'Space Mono'}, 'suffix': ''},
        gauge={
            'axis': {'range': [0, 400], 'tickwidth': 1, 'tickcolor': '#1e2a45',
                     'tickfont': {'color': '#6b7fa3', 'size': 9}},
            'bar': {'color': color, 'thickness': 0.25},
            'bgcolor': '#151d30',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50],   'color': '#00e67615'},
                {'range': [50, 100], 'color': '#ffee5815'},
                {'range': [100, 200],'color': '#ff980015'},
                {'range': [200, 300],'color': '#f4433615'},
                {'range': [300, 400],'color': '#9c27b015'},
            ],
            'threshold': {
                'line': {'color': color, 'width': 3},
                'thickness': 0.8,
                'value': aqi
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=10),
        height=220,
        font={'family': 'DM Sans'}
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
    st.markdown('<div style="font-family:Space Mono,monospace;font-size:1.1rem;font-weight:700;color:#4a9eff;letter-spacing:0.05em;padding:8px 0 4px 0;">🌫️ AQI PREDICTOR</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem;color:#6b7fa3;margin-bottom:16px;">India • 29 Cities • 24h & 48h</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📍 Location")
    city = st.selectbox("City", CITIES, index=CITIES.index("Mumbai"), label_visibility="collapsed")
    state = CITY_STATES[city]
    st.markdown(f'<div style="font-size:0.78rem;color:#4a9eff;margin:-8px 0 12px 2px;">📌 {state}</div>', unsafe_allow_html=True)

    st.markdown("### 🌤️ Weather")
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

    st.markdown("### 💨 Pollutants")
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

    festival     = st.checkbox("Festival Period")
    crop_burning = st.checkbox("Crop Burning Season")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔮  PREDICT AQI", use_container_width=True)

# ── Main panel ─────────────────────────────────────────────────────────────────
st.markdown(f'<div class="page-title">India AQI Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">AI-powered 24h & 48h air quality forecast for 29 Indian cities</div>', unsafe_allow_html=True)

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

    # ── Gauge charts ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">AQI Forecast</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(make_gauge(current_aqi, "Current AQI", info_now["color"]),
                        use_container_width=True, config={'displayModeBar': False})
    with g2:
        st.plotly_chart(make_gauge(aqi_24, "24-Hour Forecast", info_24["color"]),
                        use_container_width=True, config={'displayModeBar': False})
    with g3:
        st.plotly_chart(make_gauge(aqi_48, "48-Hour Forecast", info_48["color"]),
                        use_container_width=True, config={'displayModeBar': False})

    # ── Status cards ──────────────────────────────────────────────────────────
    d1, d2, d3 = st.columns(3)
    delta_24 = aqi_24 - current_aqi
    delta_48 = aqi_48 - current_aqi
    arrow_24 = "↑" if delta_24 > 0 else "↓" if delta_24 < 0 else "→"
    arrow_48 = "↑" if delta_48 > 0 else "↓" if delta_48 < 0 else "→"

    with d1:
        st.markdown(f"""
        <div class="metric-card {info_now['css']}">
            <div class="metric-label">Now</div>
            <div class="metric-value {info_now['css']}">{current_aqi}</div>
            <div class="metric-delta">&nbsp;</div>
            <span class="metric-badge badge-{info_now['css']}">{info_now['icon']} {risk_now}</span>
        </div>""", unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <div class="metric-card {info_24['css']}">
            <div class="metric-label">24 Hours</div>
            <div class="metric-value {info_24['css']}">{aqi_24}</div>
            <div class="metric-delta">{arrow_24} {abs(delta_24):+d} from now</div>
            <span class="metric-badge badge-{info_24['css']}">{info_24['icon']} {risk_24}</span>
        </div>""", unsafe_allow_html=True)

    with d3:
        st.markdown(f"""
        <div class="metric-card {info_48['css']}">
            <div class="metric-label">48 Hours</div>
            <div class="metric-value {info_48['css']}">{aqi_48}</div>
            <div class="metric-delta">{arrow_48} {abs(delta_48):+d} from now</div>
            <span class="metric-badge badge-{info_48['css']}">{info_48['icon']} {risk_48}</span>
        </div>""", unsafe_allow_html=True)

    # ── AQI scale bar ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">AQI Scale Reference</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="aqi-scale">
        <div class="scale-good"></div>
        <div class="scale-moderate"></div>
        <div class="scale-poor"></div>
        <div class="scale-verypoor"></div>
        <div class="scale-severe"></div>
    </div>
    <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#6b7fa3;margin-top:4px;">
        <span>✅ Good (0–50)</span>
        <span>🟡 Moderate (51–100)</span>
        <span>😷 Poor (101–200)</span>
        <span>🚨 Very Poor (201–300)</span>
        <span>☠️ Severe (300+)</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Advisory ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Health Advisory</div>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        st.markdown(f"""
        <div class="advisory-card" style="border-left: 3px solid {info_24['color']}">
            <div class="advisory-title">24-Hour Advisory</div>
            <div class="advisory-text">{info_24['icon']} {info_24['advice']}</div>
        </div>""", unsafe_allow_html=True)
    with a2:
        st.markdown(f"""
        <div class="advisory-card" style="border-left: 3px solid {info_48['color']}">
            <div class="advisory-title">48-Hour Advisory</div>
            <div class="advisory-text">{info_48['icon']} {info_48['advice']}</div>
        </div>""", unsafe_allow_html=True)

    # ── Trend bar chart ───────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Trend Overview</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=["Now", "24h Forecast", "48h Forecast"],
        y=[current_aqi, aqi_24, aqi_48],
        marker_color=[info_now['color'], info_24['color'], info_48['color']],
        marker_line_width=0,
        text=[f"{v}" for v in [current_aqi, aqi_24, aqi_48]],
        textposition='outside',
        textfont=dict(color='#e8eaf0', family='Space Mono', size=13),
        width=0.4
    ))
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=10),
        height=220,
        xaxis=dict(showgrid=False, tickfont=dict(color='#6b7fa3', family='DM Sans')),
        yaxis=dict(showgrid=True, gridcolor='#1e2a45', tickfont=dict(color='#6b7fa3'),
                   range=[0, max(current_aqi, aqi_24, aqi_48) * 1.3]),
        showlegend=False,
        bargap=0.4
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    # ── Warning banner ────────────────────────────────────────────────────────
    if risk_24 in ['Poor','Very Poor','Severe'] or risk_48 in ['Poor','Very Poor','Severe']:
        st.markdown(f"""
        <div class="warning-banner">
            ⚠️ <strong>Early Warning</strong> — Elevated pollution expected in <strong>{city}</strong>.
            24h: <strong>{risk_24}</strong> (AQI {aqi_24}) &nbsp;|&nbsp;
            48h: <strong>{risk_48}</strong> (AQI {aqi_48})<br>
            <span style="font-size:0.82rem;opacity:0.8;">Consider limiting outdoor activities and wearing a mask.</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="safe-banner">
            ✅ <strong>Air quality looks good</strong> for <strong>{city}</strong> over the next 48 hours.
            Enjoy outdoor activities!
        </div>""", unsafe_allow_html=True)

else:
    # ── Welcome screen ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon">🌫️</div>
        <div class="welcome-title">Ready to Predict</div>
        <div class="welcome-text">
            Set your city and conditions in the sidebar,<br>then click <strong>Predict AQI</strong> to get your forecast.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:32px;">AQI Scale Reference</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="aqi-scale">
        <div class="scale-good"></div><div class="scale-moderate"></div>
        <div class="scale-poor"></div><div class="scale-verypoor"></div>
        <div class="scale-severe"></div>
    </div>
    <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:#6b7fa3;margin-top:4px;">
        <span>✅ Good (0–50)</span><span>🟡 Moderate (51–100)</span>
        <span>😷 Poor (101–200)</span><span>🚨 Very Poor (201–300)</span><span>☠️ Severe (300+)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:28px;">29 Cities Covered</div>', unsafe_allow_html=True)
    rows = [CITIES[i:i+6] for i in range(0, len(CITIES), 6)]
    for row in rows:
        cols = st.columns(6)
        for col, c in zip(cols, row):
            col.markdown(f'<div style="font-size:0.78rem;color:#6b7fa3;padding:4px 0;">{c}</div>',
                        unsafe_allow_html=True)
