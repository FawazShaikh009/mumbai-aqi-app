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

# ───────────────────────────────── CSS ─────────────────────────────────
st.markdown("""
<style>
body { background: #0b1220; color: white; }
.block-container { max-width: 1100px; }

.pred-card {
    width: 100%;
    box-sizing: border-box;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}
.pred-card-24 { background: #1e3a5f; }
.pred-card-48 { background: #5a1e1e; }

.pred-number {
    font-size: 3rem;
    font-weight: bold;
}

.character-wrap svg {
    max-width: 110px;
}

.alert {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
    font-weight: bold;
}
.alert-danger { background:#5a1e1e; color:#ffb3b3; }
.alert-warning { background:#5a3e1e; color:#ffd699; }
.alert-safe { background:#1e5a2e; color:#b6f2c2; }

</style>
""", unsafe_allow_html=True)

# ───────────────────────────────── HELPERS ─────────────────────────────
def get_risk(aqi):
    if aqi <= 50: return "Good", "#4ade80"
    elif aqi <= 100: return "Moderate", "#facc15"
    elif aqi <= 200: return "Poor", "#fb923c"
    elif aqi <= 300: return "Very Poor", "#f87171"
    else: return "Severe", "#c084fc"

def get_character_svg(aqi, gender="boy"):
    hair = "#3d2b1f" if gender=="boy" else "#7c3aed"

    if aqi <= 100:
        return f"""
        <svg width="100" height="120">
        <circle cx="50" cy="40" r="25" fill="#f4a261"/>
        <ellipse cx="50" cy="20" rx="25" ry="10" fill="{hair}"/>
        <circle cx="42" cy="38" r="3"/>
        <circle cx="58" cy="38" r="3"/>
        <path d="M40 50 Q50 60 60 50" stroke="black" fill="none"/>
        </svg>
        """
    else:
        return f"""
        <svg width="100" height="120">
        <circle cx="50" cy="40" r="25" fill="#f4a261"/>
        <ellipse cx="50" cy="20" rx="25" ry="10" fill="{hair}"/>
        <rect x="30" y="45" width="40" height="15" rx="7" fill="#ccc"/>
        </svg>
        """

# ───────────────────────────────── HEADER ─────────────────────────────
st.title("Mumbai AQI Guardian")
st.caption(datetime.now().strftime("%d %B %Y | %I:%M %p"))

# ───────────────────────────────── INPUTS ─────────────────────────────
col1, col2 = st.columns(2)

with col1:
    current_aqi = st.slider("AQI", 10, 400, 120)
    pm25 = st.slider("PM2.5", 5.0, 300.0, 60.0)

with col2:
    temp = st.slider("Temperature", 15.0, 40.0, 28.0)
    humidity = st.slider("Humidity", 20, 100, 65)

# ───────────────────────────── CHARACTER ──────────────────────────────
st.markdown("### Current Air Status")
char_svg = get_character_svg(current_aqi, "boy")
risk, color = get_risk(current_aqi)

st.markdown(f"""
<div style="display:flex;align-items:center;gap:20px;">
{char_svg}
<div>
<h3 style="color:{color};">AQI {current_aqi} - {risk}</h3>
</div>
</div>
""", unsafe_allow_html=True)

# ───────────────────────────── PREDICT ────────────────────────────────
if st.button("Predict AQI"):

    pred_24 = current_aqi + np.random.randint(-20, 25)
    pred_48 = current_aqi + np.random.randint(-30, 30)

    r24, c24 = get_risk(pred_24)
    r48, c48 = get_risk(pred_48)

    # ALERT
    if pred_48 > 200:
        st.markdown('<div class="alert alert-danger">⚠️ Dangerous AQI expected</div>', unsafe_allow_html=True)
    elif pred_48 > 100:
        st.markdown('<div class="alert alert-warning">⚠️ Moderate risk AQI</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert alert-safe">✅ Air quality acceptable</div>', unsafe_allow_html=True)

    # CARDS
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="pred-card pred-card-24">
            <h4>Next 24 Hours</h4>
            {get_character_svg(pred_24, "girl")}
            <div class="pred-number" style="color:{c24};">{int(pred_24)}</div>
            <div>{r24}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="pred-card pred-card-48">
            <h4>Next 48 Hours</h4>
            {get_character_svg(pred_48, "boy")}
            <div class="pred-number" style="color:{c48};">{int(pred_48)}</div>
            <div>{r48}</div>
        </div>
        """, unsafe_allow_html=True)

    # ───────── TREND ─────────
    st.markdown("### 7-Day AQI Trend")

    trend = []
    val = current_aqi
    for _ in range(7):
        val += np.random.randint(-15, 20)
        val = max(10, min(400, val))
        trend.append(val)

    df = pd.DataFrame({"Day": range(1,8), "AQI": trend})
    st.line_chart(df.set_index("Day"))
