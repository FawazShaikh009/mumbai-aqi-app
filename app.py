# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(
    page_title="Mumbai AQI Guardian",
    layout="wide",
    page_icon="🌬️",
    initial_sidebar_state="collapsed"
)

# ✅ FIXED CSS (escaped all curly braces)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {{ font-family: 'Sora', sans-serif; }}

header[data-testid="stHeader"] {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}
.stDeployButton {{ display: none !important; }}
div[data-testid="stToolbar"] {{ display: none !important; }}

.stApp {{
    background: linear-gradient(160deg, #0a0e1a 0%, #0d1b2e 50%, #091220 100%);
    min-height: 100vh;
}}

.block-container {{ padding: 1.5rem 1rem 2rem 1rem !important; max-width: 1100px !important; }}

@keyframes float {{
    0%   {{ transform: translateY(0px); }}
    50%  {{ transform: translateY(-8px); }}
    100% {{ transform: translateY(0px); }}
}}

@keyframes breathe {{
    0%   {{ transform: scaleX(1); }}
    50%  {{ transform: scaleX(0.96); }}
    100% {{ transform: scaleX(1); }}
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ──
def get_risk(aqi):
    if aqi <= 50: return "Good", "#68d391", "dot-green", "advice-safe"
    elif aqi <= 100: return "Moderate", "#f6e05e", "dot-yellow", "advice-caution"
    elif aqi <= 200: return "Poor", "#fbd38d", "dot-orange", "advice-caution"
    elif aqi <= 300: return "Very Poor", "#fc8181", "dot-red", "advice-danger"
    else: return "Severe", "#e9d8fd", "dot-purple", "advice-danger"

def get_health_advice(label, window):
    advice = {
        "Good": f"Conditions look great for the next {window}.",
        "Moderate": f"Sensitive individuals should limit outdoor exertion over the next {window}.",
        "Poor": f"Limit outdoor activity for the next {window}.",
        "Very Poor": f"Avoid going outside for the next {window}.",
        "Severe": f"Hazardous conditions for the next {window}. Stay indoors.",
    }
    return advice.get(label, "Monitor conditions.")

# ── Hero ──
now = datetime.now()
st.markdown(f"""
<div style="padding:20px;border-radius:12px;background:#1a3a5c;">
<h2>Mumbai AQI Guardian</h2>
<p>{now.strftime('%d %B %Y %I:%M %p')}</p>
</div>
""", unsafe_allow_html=True)

# ── Model ──
@st.cache_resource
def load_model():
    return joblib.load("mumbai_aqi_model_streamlit.pkl")

try:
    model = load_model()
    st.success("Model Ready")
except:
    model = None
    st.info("Demo mode")

# ── Inputs ──
col1, col2 = st.columns(2)
with col1:
    current_aqi = st.slider("AQI", 10, 400, 120)
    pm25 = st.slider("PM2.5", 5.0, 300.0, 60.0)
with col2:
    temp = st.slider("Temp", 15.0, 40.0, 28.0)
    humidity = st.slider("Humidity", 20, 100, 65)

# ── Predict ──
if st.button("Predict"):
    if model:
        pred = model.predict(pd.DataFrame({
            'US_AQI':[current_aqi],
            'PM2_5_ugm3':[pm25],
            'Temp_2m_C':[temp],
            'Humidity_Percent':[humidity]
        }))
        pred_24, pred_48 = pred[0]
    else:
        pred_24 = current_aqi + np.random.randint(-20,20)
        pred_48 = current_aqi + np.random.randint(-30,30)

    r24, c24, _, _ = get_risk(pred_24)
    r48, c48, _, _ = get_risk(pred_48)

    st.markdown(f"""
    <div>
        <h3 style="color:{c24}">24h AQI: {pred_24:.0f} ({r24})</h3>
        <p>{get_health_advice(r24, '24h')}</p>

        <h3 style="color:{c48}">48h AQI: {pred_48:.0f} ({r48})</h3>
        <p>{get_health_advice(r48, '48h')}</p>
    </div>
    """, unsafe_allow_html=True)
