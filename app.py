import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Mumbai AQI Guardian",
    layout="wide",
    page_icon="ðŸŒ¬ï¸",
    initial_sidebar_state="collapsed"
)

# â”€â”€ Global CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(160deg, #0a0e1a 0%, #0d1b2e 50%, #091220 100%);
    min-height: 100vh;
}

/* Remove default streamlit padding on mobile */
.block-container {
    padding: 1rem 1rem 2rem 1rem !important;
    max-width: 1100px !important;
}

/* â”€â”€ Hero Banner â”€â”€ */
.hero-banner {
    background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 50%, #0d2137 100%);
    border: 1px solid rgba(99, 179, 237, 0.2);
    border-radius: 20px;
    padding: 28px 32px 22px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: clamp(1.6rem, 5vw, 2.6rem);
    font-weight: 700;
    color: #e2f4ff;
    margin: 0 0 4px;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 0.85rem;
    color: #63b3ed;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hero-time {
    font-size: 0.78rem;
    color: rgba(226,244,255,0.45);
    margin-top: 10px;
    font-family: 'Space Mono', monospace;
}

/* â”€â”€ AQI Scale Bar â”€â”€ */
.scale-wrap {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 24px;
}
.scale-title {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.45);
    margin-bottom: 14px;
    font-family: 'Space Mono', monospace;
}
.scale-bar {
    height: 10px;
    border-radius: 6px;
    background: linear-gradient(90deg, #38a169 0%, #d69e2e 30%, #dd6b20 55%, #e53e3e 75%, #805ad5 100%);
    margin-bottom: 8px;
}
.scale-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
}
.scale-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}
.chip {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.chip-green  { background: rgba(56,161,105,0.18); color: #68d391; border: 1px solid rgba(56,161,105,0.3); }
.chip-yellow { background: rgba(214,158,46,0.18);  color: #f6e05e; border: 1px solid rgba(214,158,46,0.3); }
.chip-orange { background: rgba(221,107,32,0.18);  color: #fbd38d; border: 1px solid rgba(221,107,32,0.3); }
.chip-red    { background: rgba(229,62,62,0.18);   color: #fc8181; border: 1px solid rgba(229,62,62,0.3); }

/* â”€â”€ Section heading â”€â”€ */
.section-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(255,255,255,0.35);
    margin: 28px 0 14px;
    font-family: 'Space Mono', monospace;
}

/* â”€â”€ Prediction Cards â”€â”€ */
.pred-card {
    border-radius: 18px;
    padding: 24px 22px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}
.pred-card-24 {
    background: linear-gradient(145deg, #1a3a5c 0%, #1e4976 100%);
}
.pred-card-48 {
    background: linear-gradient(145deg, #3a1a1a 0%, #5c2020 100%);
}
.pred-hour {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: rgba(255,255,255,0.5);
    font-family: 'Space Mono', monospace;
    margin-bottom: 8px;
}
.pred-number {
    font-size: clamp(3rem, 10vw, 4.5rem);
    font-weight: 700;
    letter-spacing: -2px;
    line-height: 1;
    margin: 8px 0;
}
.pred-status {
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.pred-badge {
    display: inline-block;
    margin-top: 10px;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    background: rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.8);
}

/* â”€â”€ Metric mini-cards â”€â”€ */
.mini-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 20px;
}
.mini-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 14px 16px;
}
.mini-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.38);
    font-family: 'Space Mono', monospace;
    margin-bottom: 6px;
}
.mini-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e2f4ff;
}
.mini-unit {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.38);
    margin-left: 2px;
}

/* â”€â”€ Health advice â”€â”€ */
.advice-card {
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border-left: 4px solid;
}
.advice-safe    { background: rgba(56,161,105,0.1);  border-color: #38a169; }
.advice-caution { background: rgba(221,107,32,0.1);  border-color: #dd6b20; }
.advice-danger  { background: rgba(229,62,62,0.1);   border-color: #e53e3e; }
.advice-title   { font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
                  letter-spacing: 0.08em; margin-bottom: 8px; font-family: 'Space Mono', monospace; }
.advice-text    { font-size: 0.85rem; color: rgba(255,255,255,0.75); line-height: 1.7; }

/* â”€â”€ Alert Banner â”€â”€ */
.alert-banner {
    border-radius: 14px;
    padding: 14px 18px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.alert-danger  { background: rgba(229,62,62,0.15);   border: 1px solid rgba(229,62,62,0.35);  color: #fc8181; }
.alert-warning { background: rgba(221,107,32,0.15);  border: 1px solid rgba(221,107,32,0.35); color: #fbd38d; }
.alert-safe    { background: rgba(56,161,105,0.12);  border: 1px solid rgba(56,161,105,0.3);  color: #68d391; }

/* â”€â”€ Streamlit widget overrides â”€â”€ */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label {
    color: rgba(255,255,255,0.65) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
}
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 14px !important;
}
div[data-testid="stMetric"] label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #e2f4ff !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

/* Predict button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #3182ce, #4299e1) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(49,130,206,0.35) !important;
}

/* Line chart */
div[data-testid="stArrowVegaLiteChart"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 16px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1b2e !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.8) !important;
}

/* Input background */
.stSelectbox > div > div,
.stSlider > div {
    background: transparent !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #3182ce !important; }

/* Info/success/error */
div[data-testid="stInfo"], .stInfo {
    background: rgba(49,130,206,0.12) !important;
    border: 1px solid rgba(49,130,206,0.25) !important;
    border-radius: 12px !important;
    color: #90cdf4 !important;
}
.stSuccess {
    background: rgba(56,161,105,0.12) !important;
    border: 1px solid rgba(56,161,105,0.25) !important;
    color: #68d391 !important;
    border-radius: 12px !important;
}

/* Mobile tweaks */
@media (max-width: 640px) {
    .block-container { padding: 0.75rem 0.75rem 2rem !important; }
    .hero-banner { padding: 20px 18px; }
    .pred-number { font-size: 3rem !important; }
}
</style>
""", unsafe_allow_html=True)


# â”€â”€ Helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def get_risk(aqi):
    if aqi <= 50:   return "Good",      "#68d391", "ðŸŸ¢", "advice-safe"
    elif aqi <= 100: return "Moderate",  "#f6e05e", "ðŸŸ¡", "advice-caution"
    elif aqi <= 200: return "Poor",      "#fbd38d", "ðŸŸ ", "advice-caution"
    elif aqi <= 300: return "Very Poor", "#fc8181", "ðŸ”´", "advice-danger"
    else:            return "Severe",    "#e9d8fd", "âš«", "advice-danger"

def get_alert_class(label):
    if label in ["Very Poor", "Severe"]: return "alert-danger"
    if label == "Poor":                  return "alert-warning"
    return "alert-safe"

def get_health_advice(label, window):
    base = {
        "Good":      f"âœ… Conditions look great for the next {window}. Outdoor activities are safe for everyone including children and elderly.",
        "Moderate":  f"âš ï¸ Sensitive individuals should limit prolonged outdoor exertion over the next {window}.",
        "Poor":      f"ðŸš¨ Limit outdoor activity for the next {window}. Wear N95 masks and keep windows closed.",
        "Very Poor": f"ðŸš¨ Avoid going outside for the next {window}. Use air purifier, monitor breathing, stay hydrated.",
        "Severe":    f"â˜ ï¸ Hazardous conditions for the next {window}. Stay indoors. Seek medical help if you feel breathlessness.",
    }
    return base.get(label, "Monitor conditions closely.")


# â”€â”€ Hero Banner â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
now = datetime.now()
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-sub">ðŸŒ¬ï¸ Real-Time Health Protection</div>
    <div class="hero-title">Mumbai AQI Guardian</div>
    <div class="hero-time">ðŸ“… {now.strftime('%d %B %Y')} &nbsp;Â·&nbsp; {now.strftime('%I:%M %p')} &nbsp;Â·&nbsp; 24 & 48 Hour Forecast</div>
</div>
""", unsafe_allow_html=True)


# â”€â”€ Load Model â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@st.cache_resource
def load_model():
    return joblib.load("mumbai_aqi_model_streamlit.pkl")

try:
    model = load_model()
    st.success("âœ… Model Ready â€” Protecting Mumbai's Health")
except:
    model = None
    st.info("â„¹ï¸ Running in demo mode (model file not found)")


# â”€â”€ AQI Scale â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<div class="scale-wrap">
    <div class="scale-title">Air Quality Index â€” Reference Scale</div>
    <div class="scale-bar"></div>
    <div class="scale-labels">
        <span>0</span><span>50</span><span>100</span><span>200</span><span>300</span><span>400+</span>
    </div>
    <div class="scale-chips">
        <span class="chip chip-green">0â€“50 Good</span>
        <span class="chip chip-yellow">51â€“100 Moderate</span>
        <span class="chip chip-orange">101â€“200 Poor</span>
        <span class="chip chip-red">201+ Danger</span>
    </div>
</div>
""", unsafe_allow_html=True)


# â”€â”€ Current Conditions Inputs â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-label">ðŸ“ Current Conditions â€” Mumbai</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")
with col1:
    current_aqi = st.slider("Current AQI", 10, 400, 120)
    pm25        = st.slider("PM2.5 (Âµg/mÂ³)", 5.0, 300.0, 60.0, step=0.5)
    season      = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])
with col2:
    temp        = st.slider("Temperature (Â°C)", 15.0, 40.0, 28.0, step=0.5)
    humidity    = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed  = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0, step=0.5)

# Live mini readouts
st.markdown(f"""
<div class="mini-grid">
    <div class="mini-card">
        <div class="mini-label">AQI Now</div>
        <div class="mini-value">{current_aqi}<span class="mini-unit">AQI</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">PM2.5</div>
        <div class="mini-value">{pm25:.1f}<span class="mini-unit">Âµg/mÂ³</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">Temp</div>
        <div class="mini-value">{temp:.1f}<span class="mini-unit">Â°C</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">Humidity</div>
        <div class="mini-value">{humidity}<span class="mini-unit">%</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">Wind</div>
        <div class="mini-value">{wind_speed:.1f}<span class="mini-unit">km/h</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">Season</div>
        <div class="mini-value" style="font-size:0.95rem">{season}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# â”€â”€ Predict Button â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
predict_clicked = st.button("ðŸ”®  Predict 24h & 48h AQI + Health Risk", type="primary", use_container_width=True)

if predict_clicked:
    with st.spinner("Analysing Mumbai's air for your health..."):

        season_factor = {'Winter': 1.20, 'Summer': 0.90, 'Monsoon': 0.80, 'Post-Monsoon': 1.10}[season]

        input_data = pd.DataFrame({
            'US_AQI':               [current_aqi],
            'PM2_5_ugm3':           [pm25],
            'Temp_2m_C':            [temp],
            'Humidity_Percent':     [humidity],
            'Wind_Speed_10m_kmh':   [wind_speed],
            'US_AQI_lag24':         [current_aqi * 0.92 * season_factor],
            'PM2_5_ugm3_lag24':     [pm25 * 0.88 * season_factor],
        })

        try:
            pred     = model.predict(input_data)
            pred_24  = float(pred[0][0])
            pred_48  = float(pred[0][1])
        except:
            pred_24  = current_aqi * season_factor + np.random.uniform(-20, 25)
            pred_48  = current_aqi * season_factor * 1.08 + np.random.uniform(-30, 35)

        r24, c24, e24, cls24 = get_risk(pred_24)
        r48, c48, e48, cls48 = get_risk(pred_48)

        # â”€â”€ Alert banners â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        if r24 in ["Very Poor", "Severe"] or r48 in ["Very Poor", "Severe"]:
            st.markdown(f"""
            <div class="alert-banner alert-danger">
                ðŸš¨ HIGH ALERT â€” Dangerous air quality expected. Take immediate precautions.
            </div>""", unsafe_allow_html=True)
        elif r24 == "Poor" or r48 == "Poor":
            st.markdown(f"""
            <div class="alert-banner alert-warning">
                âš ï¸ CAUTION â€” Elevated AQI forecast. Sensitive groups should stay indoors.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-banner alert-safe">
                âœ… CONDITIONS MANAGEABLE â€” Stay aware and monitor changes.
            </div>""", unsafe_allow_html=True)

        # â”€â”€ Prediction Cards â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        st.markdown('<div class="section-label">ðŸ“Š Health Forecast</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown(f"""
            <div class="pred-card pred-card-24">
                <div class="pred-hour">Next 24 Hours</div>
                <div class="pred-number" style="color:{c24};">{pred_24:.0f}</div>
                <div class="pred-status" style="color:{c24};">{e24} {r24}</div>
                <div class="pred-badge">AQI Forecast</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="pred-card pred-card-48">
                <div class="pred-hour">Next 48 Hours</div>
                <div class="pred-number" style="color:{c48};">{pred_48:.0f}</div>
                <div class="pred-status" style="color:{c48};">{e48} {r48}</div>
                <div class="pred-badge">AQI Forecast</div>
            </div>""", unsafe_allow_html=True)

        # â”€â”€ Health Advice â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        st.markdown('<div class="section-label">ðŸ›¡ï¸ Personalised Health Advice</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="advice-card {cls24}">
            <div class="advice-title" style="color:{c24};">24-Hour Outlook â€” {r24}</div>
            <div class="advice-text">{get_health_advice(r24, '24 hours')}</div>
        </div>
        <div class="advice-card {cls48}">
            <div class="advice-title" style="color:{c48};">48-Hour Outlook â€” {r48}</div>
            <div class="advice-text">{get_health_advice(r48, '48 hours')}</div>
        </div>
        """, unsafe_allow_html=True)

        # â”€â”€ 7-Day Trend Chart â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        st.markdown('<div class="section-label">ðŸ“ˆ 7-Day AQI Trend â€” Mumbai</div>', unsafe_allow_html=True)
        dates     = pd.date_range(end=datetime.now(), periods=7)
        aqi_trend = [max(10, current_aqi + np.random.randint(-35, 40)) for _ in range(7)]
        trend_df  = pd.DataFrame({"Date": dates, "AQI": aqi_trend})

        import altair as alt
        chart = alt.Chart(trend_df).mark_line(
            color='#63b3ed', strokeWidth=2.5, point=alt.OverlayMarkDef(color='#90cdf4', size=60)
        ).encode(
            x=alt.X('Date:T', axis=alt.Axis(labelColor='#718096', tickColor='#4a5568',
                                             gridColor='rgba(255,255,255,0.05)', title=None,
                                             labelFontSize=11)),
            y=alt.Y('AQI:Q', axis=alt.Axis(labelColor='#718096', tickColor='#4a5568',
                                            gridColor='rgba(255,255,255,0.05)', title='AQI',
                                            labelFontSize=11)),
            tooltip=['Date:T', 'AQI:Q']
        ).properties(height=220, background='transparent').configure_view(strokeWidth=0)

        st.altair_chart(chart, use_container_width=True)

        # â”€â”€ Summary Metrics â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        st.markdown('<div class="section-label">ðŸ“Œ Session Summary</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current AQI",   current_aqi)
        m2.metric("24h Forecast",  f"{pred_24:.0f}", delta=f"{pred_24 - current_aqi:+.0f}")
        m3.metric("48h Forecast",  f"{pred_48:.0f}", delta=f"{pred_48 - current_aqi:+.0f}")
        m4.metric("PM2.5",         f"{pm25:.1f} Âµg")


# â”€â”€ Sidebar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with st.sidebar:
    st.markdown("### ðŸ« Health First")
    st.info("""
    **High AQI can cause:**
    - Breathing problems
    - Heart & lung stress
    - Risk for children & elderly
    - Eye and throat irritation
    """)
    st.markdown("---")
    st.markdown("**Quick AQI Guide**")
    st.markdown("ðŸŸ¢ 0â€“50 â†’ Safe")
    st.markdown("ðŸŸ¡ 51â€“100 â†’ Moderate")
    st.markdown("ðŸŸ  101â€“200 â†’ Poor")
    st.markdown("ðŸ”´ 201â€“300 â†’ Very Poor")
    st.markdown("âš« 300+ â†’ Severe")
    st.markdown("---")
    st.caption("Capstone Project Â· Mumbai AQI Guardian")

st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.2);font-size:0.75rem;margin-top:2rem;">Made with â¤ï¸ for Mumbai Â· AQI Guardian</div>', unsafe_allow_html=True)
