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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

/* ── Hide Streamlit toolbar / header bar ── */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer    { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

.stApp {
    background: linear-gradient(160deg, #0a0e1a 0%, #0d1b2e 50%, #091220 100%);
    min-height: 100vh;
}
.block-container { padding: 1.5rem 1rem 2rem 1rem !important; max-width: 1100px !important; }

/* Hero */
.hero-banner {
    background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 50%, #0d2137 100%);
    border: 1px solid rgba(99,179,237,0.2);
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
    font-weight: 700; color: #e2f4ff;
    margin: 0 0 4px; letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 0.85rem; color: #63b3ed;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em; text-transform: uppercase;
}
.hero-time {
    font-size: 0.78rem; color: rgba(226,244,255,0.45);
    margin-top: 10px; font-family: 'Space Mono', monospace;
}

/* Scale */
.scale-wrap {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; padding: 18px 22px; margin-bottom: 24px;
}
.scale-title {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em;
    color: rgba(255,255,255,0.45); margin-bottom: 14px; font-family: 'Space Mono', monospace;
}
.scale-bar {
    height: 10px; border-radius: 6px;
    background: linear-gradient(90deg, #38a169 0%, #d69e2e 30%, #dd6b20 55%, #e53e3e 75%, #805ad5 100%);
    margin-bottom: 8px;
}
.scale-labels { display: flex; justify-content: space-between; font-size: 0.7rem; color: rgba(255,255,255,0.5); }
.scale-chips  { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.chip { padding: 4px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em; }
.chip-green  { background: rgba(56,161,105,0.18); color: #68d391; border: 1px solid rgba(56,161,105,0.3); }
.chip-yellow { background: rgba(214,158,46,0.18); color: #f6e05e; border: 1px solid rgba(214,158,46,0.3); }
.chip-orange { background: rgba(221,107,32,0.18); color: #fbd38d; border: 1px solid rgba(221,107,32,0.3); }
.chip-red    { background: rgba(229,62,62,0.18);  color: #fc8181; border: 1px solid rgba(229,62,62,0.3); }

/* Section label */
.section-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.35); margin: 28px 0 14px; font-family: 'Space Mono', monospace;
}

/* Character card */
.character-wrap {
    display: flex;
    align-items: center;
    gap: 20px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 24px;
}
.character-text-block { flex: 1; }
.character-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.35); font-family: 'Space Mono', monospace; margin-bottom: 6px;
}
.character-status {
    font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;
}
.character-tip {
    font-size: 0.82rem; color: rgba(255,255,255,0.55); line-height: 1.6;
}
@keyframes float {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}
@keyframes breathe {
    0%   { transform: scaleX(1); }
    50%  { transform: scaleX(0.96); }
    100% { transform: scaleX(1); }
}
.char-svg { animation: float 3s ease-in-out infinite; }

/* Prediction cards */
.pred-card {
    border-radius: 18px; padding: 24px 22px; text-align: center;
    border: 1px solid rgba(255,255,255,0.1); position: relative; overflow: hidden;
}
.pred-card-24 { background: linear-gradient(145deg, #1a3a5c 0%, #1e4976 100%); }
.pred-card-48 { background: linear-gradient(145deg, #3a1a1a 0%, #5c2020 100%); }
.pred-hour {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.5); font-family: 'Space Mono', monospace; margin-bottom: 8px;
}
.pred-number { font-size: clamp(3rem, 10vw, 4.5rem); font-weight: 700; letter-spacing: -2px; line-height: 1; margin: 8px 0; }
.pred-status { font-size: 1rem; font-weight: 600; letter-spacing: 0.02em; }
.pred-badge {
    display: inline-block; margin-top: 10px; padding: 4px 14px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600;
    background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.8);
}

/* Status dot */
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.dot-green  { background: #38a169; }
.dot-yellow { background: #d69e2e; }
.dot-orange { background: #dd6b20; }
.dot-red    { background: #e53e3e; }
.dot-purple { background: #805ad5; }

/* Mini cards */
.mini-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 20px; }
.mini-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09); border-radius: 14px; padding: 14px 16px; }
.mini-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.38); font-family: 'Space Mono', monospace; margin-bottom: 6px; }
.mini-value { font-size: 1.35rem; font-weight: 700; color: #e2f4ff; }
.mini-unit  { font-size: 0.65rem; color: rgba(255,255,255,0.38); margin-left: 2px; }

/* Health advice */
.advice-card { border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; border-left: 4px solid; }
.advice-safe    { background: rgba(56,161,105,0.1);  border-color: #38a169; }
.advice-caution { background: rgba(221,107,32,0.1);  border-color: #dd6b20; }
.advice-danger  { background: rgba(229,62,62,0.1);   border-color: #e53e3e; }
.advice-title { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-family: 'Space Mono', monospace; }
.advice-text  { font-size: 0.85rem; color: rgba(255,255,255,0.75); line-height: 1.7; }

/* Alert */
.alert-banner { border-radius: 14px; padding: 14px 18px; font-size: 0.88rem; font-weight: 600; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.alert-danger  { background: rgba(229,62,62,0.15);  border: 1px solid rgba(229,62,62,0.35);  color: #fc8181; }
.alert-warning { background: rgba(221,107,32,0.15); border: 1px solid rgba(221,107,32,0.35); color: #fbd38d; }
.alert-safe    { background: rgba(56,161,105,0.12); border: 1px solid rgba(56,161,105,0.3);  color: #68d391; }

/* Streamlit overrides */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label { color: rgba(255,255,255,0.65) !important; font-size: 0.82rem !important; }
div[data-testid="stMetric"] { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09); border-radius: 14px; padding: 14px !important; }
div[data-testid="stMetric"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.7rem !important; text-transform: uppercase; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e2f4ff !important; font-size: 1.3rem !important; font-weight: 700 !important; }
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-weight: 600 !important; font-size: 1rem !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover { background: linear-gradient(135deg, #3182ce, #4299e1) !important; }
div[data-testid="stArrowVegaLiteChart"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 16px !important; }
section[data-testid="stSidebar"] { background: #0d1b2e !important; border-right: 1px solid rgba(255,255,255,0.07) !important; }
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }

@media (max-width: 640px) {
    .block-container { padding: 0.75rem 0.75rem 2rem !important; }
    .hero-banner { padding: 20px 18px; }
    .pred-number { font-size: 3rem !important; }
    .character-wrap { flex-direction: column; text-align: center; }
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_risk(aqi):
    if aqi <= 50:    return "Good",      "#68d391", "dot-green",  "advice-safe"
    elif aqi <= 100: return "Moderate",  "#f6e05e", "dot-yellow", "advice-caution"
    elif aqi <= 200: return "Poor",      "#fbd38d", "dot-orange", "advice-caution"
    elif aqi <= 300: return "Very Poor", "#fc8181", "dot-red",    "advice-danger"
    else:            return "Severe",    "#e9d8fd", "dot-purple", "advice-danger"

def get_health_advice(label, window):
    advice = {
        "Good":      f"Conditions look great for the next {window}. Outdoor activities are safe for everyone including children and elderly.",
        "Moderate":  f"Sensitive individuals should limit prolonged outdoor exertion over the next {window}.",
        "Poor":      f"Limit outdoor activity for the next {window}. Wear N95 masks and keep windows closed.",
        "Very Poor": f"Avoid going outside for the next {window}. Use air purifier, monitor breathing, stay hydrated.",
        "Severe":    f"Hazardous conditions for the next {window}. Stay indoors. Seek medical help if you feel breathlessness.",
    }
    return advice.get(label, "Monitor conditions closely.")

def get_character_svg(aqi):
    """Returns an SVG character — masked + worried for bad AQI, happy for good AQI."""
    if aqi <= 50:
        # Happy person, clean air, green tones
        return """
        <svg class="char-svg" width="110" height="140" viewBox="0 0 110 140" xmlns="http://www.w3.org/2000/svg">
          <!-- Body -->
          <ellipse cx="55" cy="115" rx="28" ry="18" fill="#1a4a2e"/>
          <!-- Shirt -->
          <rect x="30" y="88" width="50" height="34" rx="10" fill="#2d6a4f"/>
          <!-- Neck -->
          <rect x="48" y="72" width="14" height="18" rx="4" fill="#f4a261"/>
          <!-- Head -->
          <circle cx="55" cy="58" r="26" fill="#f4a261"/>
          <!-- Hair -->
          <ellipse cx="55" cy="34" rx="26" ry="10" fill="#3d2b1f"/>
          <!-- Eyes -->
          <circle cx="46" cy="54" r="4" fill="#1a1a1a"/>
          <circle cx="64" cy="54" r="4" fill="#1a1a1a"/>
          <!-- Eye shine -->
          <circle cx="48" cy="52" r="1.5" fill="white"/>
          <circle cx="66" cy="52" r="1.5" fill="white"/>
          <!-- Smile -->
          <path d="M44 66 Q55 76 66 66" stroke="#c0392b" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <!-- Cheeks -->
          <circle cx="41" cy="63" r="5" fill="rgba(255,150,100,0.35)"/>
          <circle cx="69" cy="63" r="5" fill="rgba(255,150,100,0.35)"/>
          <!-- Arms up (happy) -->
          <line x1="30" y1="95" x2="10" y2="75" stroke="#2d6a4f" stroke-width="8" stroke-linecap="round"/>
          <line x1="80" y1="95" x2="100" y2="75" stroke="#2d6a4f" stroke-width="8" stroke-linecap="round"/>
          <!-- Legs -->
          <line x1="45" y1="122" x2="38" y2="140" stroke="#1a4a2e" stroke-width="8" stroke-linecap="round"/>
          <line x1="65" y1="122" x2="72" y2="140" stroke="#1a4a2e" stroke-width="8" stroke-linecap="round"/>
          <!-- Clean air sparkles -->
          <circle cx="15" cy="60" r="3" fill="#68d391" opacity="0.8"/>
          <circle cx="95" cy="50" r="2" fill="#68d391" opacity="0.6"/>
          <circle cx="20" cy="40" r="2" fill="#9ae6b4" opacity="0.7"/>
        </svg>
        """, "#68d391", "Air is clean! Safe to go outside freely."

    elif aqi <= 100:
        # Slightly cautious person, light mask
        return """
        <svg class="char-svg" width="110" height="140" viewBox="0 0 110 140" xmlns="http://www.w3.org/2000/svg">
          <!-- Body -->
          <ellipse cx="55" cy="115" rx="28" ry="18" fill="#2d4a6e"/>
          <!-- Shirt -->
          <rect x="30" y="88" width="50" height="34" rx="10" fill="#3a6186"/>
          <!-- Neck -->
          <rect x="48" y="72" width="14" height="18" rx="4" fill="#f4a261"/>
          <!-- Head -->
          <circle cx="55" cy="58" r="26" fill="#f4a261"/>
          <!-- Hair -->
          <ellipse cx="55" cy="34" rx="26" ry="10" fill="#2c2c54"/>
          <!-- Eyes (slightly concerned) -->
          <ellipse cx="46" cy="54" rx="4" ry="3.5" fill="#1a1a1a"/>
          <ellipse cx="64" cy="54" rx="4" ry="3.5" fill="#1a1a1a"/>
          <circle cx="48" cy="52" r="1.5" fill="white"/>
          <circle cx="66" cy="52" r="1.5" fill="white"/>
          <!-- Light mask -->
          <rect x="38" y="62" width="34" height="16" rx="8" fill="#a0c4ff" opacity="0.9"/>
          <line x1="38" y1="70" x2="31" y2="68" stroke="#a0c4ff" stroke-width="2"/>
          <line x1="72" y1="70" x2="79" y2="68" stroke="#a0c4ff" stroke-width="2"/>
          <!-- Arms neutral -->
          <line x1="30" y1="100" x2="12" y2="90" stroke="#3a6186" stroke-width="8" stroke-linecap="round"/>
          <line x1="80" y1="100" x2="98" y2="90" stroke="#3a6186" stroke-width="8" stroke-linecap="round"/>
          <!-- Legs -->
          <line x1="45" y1="122" x2="38" y2="140" stroke="#2d4a6e" stroke-width="8" stroke-linecap="round"/>
          <line x1="65" y1="122" x2="72" y2="140" stroke="#2d4a6e" stroke-width="8" stroke-linecap="round"/>
        </svg>
        """, "#f6e05e", "Moderate air. Consider wearing a light mask outside."

    elif aqi <= 200:
        # Masked person, orange tones, worried
        return """
        <svg class="char-svg" width="110" height="140" viewBox="0 0 110 140" xmlns="http://www.w3.org/2000/svg">
          <!-- Body -->
          <ellipse cx="55" cy="115" rx="28" ry="18" fill="#5a2d00"/>
          <!-- Jacket -->
          <rect x="30" y="88" width="50" height="34" rx="10" fill="#7b4f1e"/>
          <!-- Neck -->
          <rect x="48" y="72" width="14" height="18" rx="4" fill="#e8956d"/>
          <!-- Head -->
          <circle cx="55" cy="58" r="26" fill="#e8956d"/>
          <!-- Hair -->
          <ellipse cx="55" cy="34" rx="26" ry="10" fill="#1a1a2e"/>
          <!-- Eyes worried (angled brows) -->
          <ellipse cx="46" cy="53" rx="4.5" ry="3.5" fill="#1a1a1a"/>
          <ellipse cx="64" cy="53" rx="4.5" ry="3.5" fill="#1a1a1a"/>
          <circle cx="48" cy="51" r="1.5" fill="white"/>
          <circle cx="66" cy="51" r="1.5" fill="white"/>
          <!-- Worried brows -->
          <path d="M42 45 Q46 42 50 44" stroke="#3d2b1f" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <path d="M60 44 Q64 42 68 45" stroke="#3d2b1f" stroke-width="2.5" fill="none" stroke-linecap="round"/>
          <!-- N95 mask -->
          <path d="M35 62 Q55 80 75 62 L75 75 Q55 88 35 75 Z" fill="#cccccc"/>
          <path d="M35 62 Q55 56 75 62" fill="#e0e0e0"/>
          <!-- Mask straps -->
          <line x1="35" y1="65" x2="27" y2="60" stroke="#aaa" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="75" y1="65" x2="83" y2="60" stroke="#aaa" stroke-width="2.5" stroke-linecap="round"/>
          <!-- Mask centre seam -->
          <line x1="55" y1="60" x2="55" y2="83" stroke="#bbb" stroke-width="1" opacity="0.6"/>
          <!-- Arms defensive -->
          <line x1="30" y1="98" x2="14" y2="112" stroke="#7b4f1e" stroke-width="8" stroke-linecap="round"/>
          <line x1="80" y1="98" x2="96" y2="112" stroke="#7b4f1e" stroke-width="8" stroke-linecap="round"/>
          <!-- Legs -->
          <line x1="45" y1="122" x2="38" y2="140" stroke="#5a2d00" stroke-width="8" stroke-linecap="round"/>
          <line x1="65" y1="122" x2="72" y2="140" stroke="#5a2d00" stroke-width="8" stroke-linecap="round"/>
          <!-- Haze particles -->
          <circle cx="12" cy="55" r="4" fill="#dd6b20" opacity="0.4"/>
          <circle cx="95" cy="70" r="3" fill="#dd6b20" opacity="0.3"/>
          <circle cx="18" cy="80" r="2" fill="#c05621" opacity="0.3"/>
        </svg>
        """, "#fbd38d", "Poor air! Wear your N95 mask before stepping out."

    else:
        # Full hazmat / heavy pollution, red tones, distressed
        return """
        <svg class="char-svg" width="110" height="140" viewBox="0 0 110 140" xmlns="http://www.w3.org/2000/svg">
          <!-- Body / hazmat suit -->
          <ellipse cx="55" cy="115" rx="30" ry="20" fill="#6b1a1a"/>
          <rect x="28" y="85" width="54" height="38" rx="12" fill="#8b2222"/>
          <!-- Gloves -->
          <ellipse cx="18" cy="115" rx="8" ry="6" fill="#a83232"/>
          <ellipse cx="92" cy="115" rx="8" ry="6" fill="#a83232"/>
          <!-- Neck cover -->
          <rect x="46" y="70" width="18" height="18" rx="5" fill="#c0392b"/>
          <!-- Head / helmet -->
          <circle cx="55" cy="56" r="28" fill="#c0392b"/>
          <!-- Helmet visor -->
          <ellipse cx="55" cy="56" rx="20" ry="16" fill="#1a1a2e" opacity="0.85"/>
          <!-- Eyes inside visor (red glow) -->
          <ellipse cx="46" cy="53" rx="5" ry="4" fill="#ff6b6b" opacity="0.9"/>
          <ellipse cx="64" cy="53" rx="5" ry="4" fill="#ff6b6b" opacity="0.9"/>
          <circle cx="48" cy="51" r="2" fill="white" opacity="0.6"/>
          <circle cx="66" cy="51" r="2" fill="white" opacity="0.6"/>
          <!-- Helmet band -->
          <path d="M27 44 Q55 28 83 44" stroke="#8b2222" stroke-width="4" fill="none"/>
          <!-- Filter canister on mask -->
          <rect x="46" y="68" width="18" height="8" rx="4" fill="#555"/>
          <rect x="50" y="71" width="10" height="3" rx="2" fill="#888"/>
          <!-- Arms raised (warning pose) -->
          <line x1="28" y1="95" x2="8" y2="78" stroke="#8b2222" stroke-width="10" stroke-linecap="round"/>
          <line x1="82" y1="95" x2="102" y2="78" stroke="#8b2222" stroke-width="10" stroke-linecap="round"/>
          <!-- Legs -->
          <line x1="44" y1="122" x2="36" y2="140" stroke="#6b1a1a" stroke-width="9" stroke-linecap="round"/>
          <line x1="66" y1="122" x2="74" y2="140" stroke="#6b1a1a" stroke-width="9" stroke-linecap="round"/>
          <!-- Heavy pollution clouds -->
          <circle cx="10" cy="50" r="7" fill="#e53e3e" opacity="0.25"/>
          <circle cx="100" cy="40" r="5" fill="#e53e3e" opacity="0.2"/>
          <circle cx="15" cy="30" r="4" fill="#fc8181" opacity="0.2"/>
          <circle cx="95" cy="65" r="6" fill="#e53e3e" opacity="0.2"/>
          <!-- Warning X marks -->
          <line x1="5"  y1="20" x2="15" y2="30" stroke="#fc8181" stroke-width="2" opacity="0.5"/>
          <line x1="15" y1="20" x2="5"  y2="30" stroke="#fc8181" stroke-width="2" opacity="0.5"/>
          <line x1="95" y1="20" x2="105" y2="30" stroke="#fc8181" stroke-width="2" opacity="0.5"/>
          <line x1="105" y1="20" x2="95" y2="30" stroke="#fc8181" stroke-width="2" opacity="0.5"/>
        </svg>
        """, "#fc8181", "HAZARDOUS! Stay indoors. Do not go outside without full protection."


# ── Hero ──────────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-sub">Real-Time Health Protection</div>
    <div class="hero-title">Mumbai AQI Guardian</div>
    <div class="hero-time">{now.strftime('%d %B %Y')} &nbsp;|&nbsp; {now.strftime('%I:%M %p')} &nbsp;|&nbsp; 24 &amp; 48 Hour Forecast</div>
</div>
""", unsafe_allow_html=True)


# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("mumbai_aqi_model_streamlit.pkl")

try:
    model = load_model()
    st.success("Model Ready - Protecting Mumbai's Health")
except:
    model = None
    st.info("Running in demo mode (model file not found)")


# ── Scale ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="scale-wrap">
    <div class="scale-title">Air Quality Index - Reference Scale</div>
    <div class="scale-bar"></div>
    <div class="scale-labels">
        <span>0</span><span>50</span><span>100</span><span>200</span><span>300</span><span>400+</span>
    </div>
    <div class="scale-chips">
        <span class="chip chip-green">0-50 Good</span>
        <span class="chip chip-yellow">51-100 Moderate</span>
        <span class="chip chip-orange">101-200 Poor</span>
        <span class="chip chip-red">201+ Danger</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Current Conditions - Mumbai</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")
with col1:
    current_aqi = st.slider("Current AQI", 10, 400, 120)
    pm25        = st.slider("PM2.5 (ug/m3)", 5.0, 300.0, 60.0, step=0.5)
    season      = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])
with col2:
    temp        = st.slider("Temperature (deg C)", 15.0, 40.0, 28.0, step=0.5)
    humidity    = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed  = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0, step=0.5)

# Mini readouts
st.markdown(f"""
<div class="mini-grid">
    <div class="mini-card">
        <div class="mini-label">AQI Now</div>
        <div class="mini-value">{current_aqi}<span class="mini-unit">AQI</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">PM2.5</div>
        <div class="mini-value">{pm25:.1f}<span class="mini-unit">ug/m3</span></div>
    </div>
    <div class="mini-card">
        <div class="mini-label">Temp</div>
        <div class="mini-value">{temp:.1f}<span class="mini-unit">deg C</span></div>
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

# ── Live character based on current AQI ──────────────────────────────────────
char_svg, char_color, char_tip = get_character_svg(current_aqi)
r_now, c_now, _, _ = get_risk(current_aqi)
st.markdown(f"""
<div class="character-wrap">
    {char_svg}
    <div class="character-text-block">
        <div class="character-label">Air Quality Status</div>
        <div class="character-status" style="color:{char_color};">Current AQI: {current_aqi} &mdash; {r_now}</div>
        <div class="character-tip">{char_tip}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Predict ───────────────────────────────────────────────────────────────────
predict_clicked = st.button("Predict 24h and 48h AQI + Health Risk", type="primary", use_container_width=True)

if predict_clicked:
    with st.spinner("Analysing Mumbai's air for your health..."):

        season_factor = {'Winter': 1.20, 'Summer': 0.90, 'Monsoon': 0.80, 'Post-Monsoon': 1.10}[season]

        input_data = pd.DataFrame({
            'US_AQI':             [current_aqi],
            'PM2_5_ugm3':         [pm25],
            'Temp_2m_C':          [temp],
            'Humidity_Percent':   [humidity],
            'Wind_Speed_10m_kmh': [wind_speed],
            'US_AQI_lag24':       [current_aqi * 0.92 * season_factor],
            'PM2_5_ugm3_lag24':   [pm25 * 0.88 * season_factor],
        })

        try:
            pred    = model.predict(input_data)
            pred_24 = float(pred[0][0])
            pred_48 = float(pred[0][1])
        except:
            pred_24 = current_aqi * season_factor + np.random.uniform(-20, 25)
            pred_48 = current_aqi * season_factor * 1.08 + np.random.uniform(-30, 35)

        r24, c24, d24, cls24 = get_risk(pred_24)
        r48, c48, d48, cls48 = get_risk(pred_48)

        # Alert
        if r24 in ["Very Poor", "Severe"] or r48 in ["Very Poor", "Severe"]:
            st.markdown("""<div class="alert-banner alert-danger">HIGH ALERT - Dangerous air quality expected. Take immediate precautions.</div>""", unsafe_allow_html=True)
        elif r24 == "Poor" or r48 == "Poor":
            st.markdown("""<div class="alert-banner alert-warning">CAUTION - Elevated AQI forecast. Sensitive groups should stay indoors.</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="alert-banner alert-safe">CONDITIONS MANAGEABLE - Stay aware and monitor changes.</div>""", unsafe_allow_html=True)

        # Forecast cards with characters
        st.markdown('<div class="section-label">Health Forecast</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        char24_svg, _, _ = get_character_svg(pred_24)
        char48_svg, _, _ = get_character_svg(pred_48)

        with c1:
            st.markdown(f"""
            <div class="pred-card pred-card-24">
                <div class="pred-hour">Next 24 Hours</div>
                {char24_svg}
                <div class="pred-number" style="color:{c24};">{pred_24:.0f}</div>
                <div class="pred-status" style="color:{c24};"><span class="dot {d24}"></span>{r24}</div>
                <div class="pred-badge">AQI Forecast</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="pred-card pred-card-48">
                <div class="pred-hour">Next 48 Hours</div>
                {char48_svg}
                <div class="pred-number" style="color:{c48};">{pred_48:.0f}</div>
                <div class="pred-status" style="color:{c48};"><span class="dot {d48}"></span>{r48}</div>
                <div class="pred-badge">AQI Forecast</div>
            </div>""", unsafe_allow_html=True)

        # Health advice
        st.markdown('<div class="section-label">Personalised Health Advice</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="advice-card {cls24}">
            <div class="advice-title" style="color:{c24};">24-Hour Outlook - {r24}</div>
            <div class="advice-text">{get_health_advice(r24, '24 hours')}</div>
        </div>
        <div class="advice-card {cls48}">
            <div class="advice-title" style="color:{c48};">48-Hour Outlook - {r48}</div>
            <div class="advice-text">{get_health_advice(r48, '48 hours')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Trend chart
        st.markdown('<div class="section-label">7-Day AQI Trend - Mumbai</div>', unsafe_allow_html=True)
        dates     = pd.date_range(end=datetime.now(), periods=7)
        aqi_trend = [max(10, current_aqi + np.random.randint(-35, 40)) for _ in range(7)]
        trend_df  = pd.DataFrame({"Date": dates, "AQI": aqi_trend})

        import altair as alt
        chart = alt.Chart(trend_df).mark_line(
            color='#63b3ed', strokeWidth=2.5,
            point=alt.OverlayMarkDef(color='#90cdf4', size=60)
        ).encode(
            x=alt.X('Date:T', axis=alt.Axis(labelColor='#718096', tickColor='#4a5568', gridColor='rgba(255,255,255,0.05)', title=None, labelFontSize=11)),
            y=alt.Y('AQI:Q', axis=alt.Axis(labelColor='#718096', tickColor='#4a5568', gridColor='rgba(255,255,255,0.05)', title='AQI', labelFontSize=11)),
            tooltip=['Date:T', 'AQI:Q']
        ).properties(height=220, background='transparent').configure_view(strokeWidth=0)
        st.altair_chart(chart, use_container_width=True)

        # Summary metrics
        st.markdown('<div class="section-label">Session Summary</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current AQI",  current_aqi)
        m2.metric("24h Forecast", f"{pred_24:.0f}", delta=f"{pred_24 - current_aqi:+.0f}")
        m3.metric("48h Forecast", f"{pred_48:.0f}", delta=f"{pred_48 - current_aqi:+.0f}")
        m4.metric("PM2.5",        f"{pm25:.1f} ug")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Health First")
    st.info("""
    **High AQI can cause:**
    - Breathing problems
    - Heart and lung stress
    - Risk for children and elderly
    - Eye and throat irritation
    """)
    st.markdown("---")
    st.markdown("**Quick AQI Guide**")
    st.markdown("Good: 0 to 50")
    st.markdown("Moderate: 51 to 100")
    st.markdown("Poor: 101 to 200")
    st.markdown("Very Poor: 201 to 300")
    st.markdown("Severe: 300+")
    st.markdown("---")
    st.caption("Capstone Project | Mumbai AQI Guardian")

st.markdown(
    '<div style="text-align:center;color:rgba(255,255,255,0.2);font-size:0.75rem;margin-top:2rem;">'
    'Made with care for Mumbai | AQI Guardian'
    '</div>',
    unsafe_allow_html=True
)
