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

header { visibility: hidden !important; height: 0 !important; }
header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }
.styles_viewerBadge__1yB5_ { display: none !important; }

.stApp {
    background: linear-gradient(160deg, #0a0e1a 0%, #0d1b2e 50%, #091220 100%);
    min-height: 100vh;
}
.block-container { padding: 1.5rem 1rem 2rem 1rem !important; max-width: 1100px !important; }

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

.section-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.35); margin: 28px 0 14px; font-family: 'Space Mono', monospace;
}

.character-wrap {
    display: flex; align-items: center; gap: 20px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px; padding: 20px 24px; margin-bottom: 24px;
}
.character-text-block { flex: 1; }
.character-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.35); font-family: 'Space Mono', monospace; margin-bottom: 6px;
}
.character-status { font-size: 1.3rem; font-weight: 700; margin-bottom: 4px; }
.character-tip { font-size: 0.82rem; color: rgba(255,255,255,0.55); line-height: 1.6; }

@keyframes float {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}
.char-svg { animation: float 3s ease-in-out infinite; display: block; margin: 0 auto 8px; }

.pred-card {
    border-radius: 18px; padding: 20px 18px; text-align: center;
    border: 1px solid rgba(255,255,255,0.1); position: relative; overflow: hidden;
    min-height: 320px;
}
.pred-card-24 { background: linear-gradient(145deg, #1a3a5c 0%, #1e4976 100%); }
.pred-card-48 { background: linear-gradient(145deg, #3a1a1a 0%, #5c2020 100%); }
.pred-hour {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.5); font-family: 'Space Mono', monospace; margin-bottom: 8px;
}
.pred-number { font-size: clamp(2.5rem, 8vw, 4rem); font-weight: 700; letter-spacing: -2px; line-height: 1; margin: 6px 0; }
.pred-status { font-size: 1rem; font-weight: 600; letter-spacing: 0.02em; }
.pred-badge {
    display: inline-block; margin-top: 10px; padding: 4px 14px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600;
    background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.8);
}

.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.dot-green  { background: #38a169; }
.dot-yellow { background: #d69e2e; }
.dot-orange { background: #dd6b20; }
.dot-red    { background: #e53e3e; }
.dot-purple { background: #805ad5; }

.mini-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin-bottom: 20px; }
.mini-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09); border-radius: 14px; padding: 14px 16px; }
.mini-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.38); font-family: 'Space Mono', monospace; margin-bottom: 6px; }
.mini-value { font-size: 1.25rem; font-weight: 700; color: #e2f4ff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-unit  { font-size: 0.62rem; color: rgba(255,255,255,0.38); margin-left: 2px; }

.advice-card { border-radius: 16px; padding: 18px 20px; margin-bottom: 12px; border-left: 4px solid; }
.advice-safe    { background: rgba(56,161,105,0.1);  border-color: #38a169; }
.advice-caution { background: rgba(221,107,32,0.1);  border-color: #dd6b20; }
.advice-danger  { background: rgba(229,62,62,0.1);   border-color: #e53e3e; }
.advice-title { font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-family: 'Space Mono', monospace; }
.advice-text  { font-size: 0.85rem; color: rgba(255,255,255,0.75); line-height: 1.7; }

.alert-banner { border-radius: 14px; padding: 14px 18px; font-size: 0.88rem; font-weight: 600; margin-bottom: 18px; }
.alert-danger  { background: rgba(229,62,62,0.15);  border: 1px solid rgba(229,62,62,0.35);  color: #fc8181; }
.alert-warning { background: rgba(221,107,32,0.15); border: 1px solid rgba(221,107,32,0.35); color: #fbd38d; }
.alert-safe    { background: rgba(56,161,105,0.12); border: 1px solid rgba(56,161,105,0.3);  color: #68d391; }

div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label { color: rgba(255,255,255,0.65) !important; font-size: 0.82rem !important; }
div[data-testid="stMetric"] { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09); border-radius: 14px; padding: 14px !important; }
div[data-testid="stMetric"] label { color: rgba(255,255,255,0.45) !important; font-size: 0.7rem !important; text-transform: uppercase; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #e2f4ff !important; font-size: 1.3rem !important; font-weight: 700 !important; }
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-weight: 600 !important; font-size: 1rem !important; width: 100% !important; padding: 0.7rem !important;
}
div[data-testid="stButton"] > button:hover { background: linear-gradient(135deg, #3182ce, #4299e1) !important; }
div[data-testid="stArrowVegaLiteChart"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 16px !important; padding: 16px !important; }
section[data-testid="stSidebar"] { background: #0d1b2e !important; border-right: 1px solid rgba(255,255,255,0.07) !important; }
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }

@media (max-width: 640px) {
    .block-container { padding: 0.75rem 0.75rem 2rem !important; }
    .hero-banner { padding: 20px 18px; }
    .pred-number { font-size: 2.5rem !important; }
    .character-wrap { flex-direction: column; text-align: center; }
    .mini-grid { grid-template-columns: repeat(3, 1fr); }
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


def boy_svg(aqi):
    """BOY character - used for 24h forecast and current status"""
    if aqi <= 50:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect x="26" y="82" width="48" height="32" rx="9" fill="#2d6a4f"/>
<ellipse cx="50" cy="110" rx="26" ry="16" fill="#1a4a2e"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#f4a261"/>
<circle cx="50" cy="54" r="24" fill="#f4a261"/>
<ellipse cx="50" cy="32" rx="24" ry="9" fill="#3d2b1f"/>
<circle cx="42" cy="50" r="3.5" fill="#1a1a1a"/>
<circle cx="58" cy="50" r="3.5" fill="#1a1a1a"/>
<circle cx="43.5" cy="48.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="48.5" r="1.5" fill="white"/>
<path d="M41 62 Q50 71 59 62" stroke="#c0392b" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<circle cx="37" cy="59" r="4" fill="rgba(255,150,100,0.3)"/>
<circle cx="63" cy="59" r="4" fill="rgba(255,150,100,0.3)"/>
<line x1="26" y1="89" x2="8" y2="70" stroke="#2d6a4f" stroke-width="7" stroke-linecap="round"/>
<line x1="74" y1="89" x2="92" y2="70" stroke="#2d6a4f" stroke-width="7" stroke-linecap="round"/>
<line x1="41" y1="116" x2="35" y2="130" stroke="#1a4a2e" stroke-width="7" stroke-linecap="round"/>
<line x1="59" y1="116" x2="65" y2="130" stroke="#1a4a2e" stroke-width="7" stroke-linecap="round"/>
<circle cx="12" cy="55" r="3" fill="#68d391" opacity="0.8"/>
<circle cx="88" cy="46" r="2" fill="#68d391" opacity="0.6"/>
<circle cx="16" cy="37" r="2" fill="#9ae6b4" opacity="0.7"/>
</svg>""", "#68d391", "Air is clean! Safe to go outside freely."

    elif aqi <= 100:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect x="26" y="82" width="48" height="32" rx="9" fill="#3a6186"/>
<ellipse cx="50" cy="110" rx="26" ry="16" fill="#2d4a6e"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#f4a261"/>
<circle cx="50" cy="54" r="24" fill="#f4a261"/>
<ellipse cx="50" cy="32" rx="24" ry="9" fill="#2c2c54"/>
<ellipse cx="42" cy="50" rx="3.5" ry="3" fill="#1a1a1a"/>
<ellipse cx="58" cy="50" rx="3.5" ry="3" fill="#1a1a1a"/>
<circle cx="43.5" cy="48.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="48.5" r="1.5" fill="white"/>
<rect x="34" y="58" width="32" height="14" rx="7" fill="#a0c4ff" opacity="0.9"/>
<line x1="34" y1="65" x2="27" y2="63" stroke="#a0c4ff" stroke-width="2"/>
<line x1="66" y1="65" x2="73" y2="63" stroke="#a0c4ff" stroke-width="2"/>
<line x1="26" y1="93" x2="10" y2="84" stroke="#3a6186" stroke-width="7" stroke-linecap="round"/>
<line x1="74" y1="93" x2="90" y2="84" stroke="#3a6186" stroke-width="7" stroke-linecap="round"/>
<line x1="41" y1="116" x2="35" y2="130" stroke="#2d4a6e" stroke-width="7" stroke-linecap="round"/>
<line x1="59" y1="116" x2="65" y2="130" stroke="#2d4a6e" stroke-width="7" stroke-linecap="round"/>
</svg>""", "#f6e05e", "Moderate air. Consider a light mask outside."

    elif aqi <= 200:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect x="26" y="82" width="48" height="32" rx="9" fill="#7b4f1e"/>
<ellipse cx="50" cy="110" rx="26" ry="16" fill="#5a2d00"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#e8956d"/>
<circle cx="50" cy="54" r="24" fill="#e8956d"/>
<ellipse cx="50" cy="32" rx="24" ry="9" fill="#1a1a2e"/>
<ellipse cx="42" cy="49" rx="4" ry="3" fill="#1a1a1a"/>
<ellipse cx="58" cy="49" rx="4" ry="3" fill="#1a1a1a"/>
<circle cx="43.5" cy="47.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="47.5" r="1.5" fill="white"/>
<path d="M39 41 Q42 38 46 40" stroke="#3d2b1f" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M54 40 Q58 38 61 41" stroke="#3d2b1f" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M32 58 Q50 74 68 58 L68 70 Q50 84 32 70 Z" fill="#cccccc"/>
<path d="M32 58 Q50 53 68 58" fill="#e0e0e0"/>
<line x1="32" y1="61" x2="24" y2="56" stroke="#aaa" stroke-width="2" stroke-linecap="round"/>
<line x1="68" y1="61" x2="76" y2="56" stroke="#aaa" stroke-width="2" stroke-linecap="round"/>
<line x1="26" y1="92" x2="11" y2="105" stroke="#7b4f1e" stroke-width="7" stroke-linecap="round"/>
<line x1="74" y1="92" x2="89" y2="105" stroke="#7b4f1e" stroke-width="7" stroke-linecap="round"/>
<line x1="41" y1="116" x2="35" y2="130" stroke="#5a2d00" stroke-width="7" stroke-linecap="round"/>
<line x1="59" y1="116" x2="65" y2="130" stroke="#5a2d00" stroke-width="7" stroke-linecap="round"/>
<circle cx="10" cy="52" r="4" fill="#dd6b20" opacity="0.35"/>
<circle cx="88" cy="64" r="3" fill="#dd6b20" opacity="0.25"/>
</svg>""", "#fbd38d", "Poor air! Wear your N95 mask before stepping out."

    else:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect x="24" y="80" width="52" height="36" rx="11" fill="#8b2222"/>
<ellipse cx="50" cy="112" rx="28" ry="18" fill="#6b1a1a"/>
<ellipse cx="15" cy="110" rx="7" ry="5" fill="#a83232"/>
<ellipse cx="85" cy="110" rx="7" ry="5" fill="#a83232"/>
<rect x="43" y="67" width="14" height="15" rx="4" fill="#c0392b"/>
<circle cx="50" cy="52" r="26" fill="#c0392b"/>
<ellipse cx="50" cy="52" rx="18" ry="14" fill="#1a1a2e" opacity="0.85"/>
<ellipse cx="42" cy="49" rx="4.5" ry="3.5" fill="#ff6b6b" opacity="0.9"/>
<ellipse cx="58" cy="49" rx="4.5" ry="3.5" fill="#ff6b6b" opacity="0.9"/>
<circle cx="44" cy="47" r="2" fill="white" opacity="0.6"/>
<circle cx="60" cy="47" r="2" fill="white" opacity="0.6"/>
<path d="M24 40 Q50 25 76 40" stroke="#8b2222" stroke-width="4" fill="none"/>
<rect x="42" y="64" width="16" height="7" rx="3" fill="#555"/>
<rect x="46" y="67" width="8" height="2.5" rx="1.5" fill="#888"/>
<line x1="24" y1="90" x2="6" y2="74" stroke="#8b2222" stroke-width="9" stroke-linecap="round"/>
<line x1="76" y1="90" x2="94" y2="74" stroke="#8b2222" stroke-width="9" stroke-linecap="round"/>
<line x1="40" y1="118" x2="33" y2="130" stroke="#6b1a1a" stroke-width="8" stroke-linecap="round"/>
<line x1="60" y1="118" x2="67" y2="130" stroke="#6b1a1a" stroke-width="8" stroke-linecap="round"/>
<circle cx="8" cy="46" r="6" fill="#e53e3e" opacity="0.2"/>
<circle cx="92" cy="36" r="5" fill="#e53e3e" opacity="0.18"/>
</svg>""", "#fc8181", "HAZARDOUS! Stay indoors. Do not go outside without full protection."


def girl_svg(aqi):
    """GIRL character - used for 48h forecast"""
    if aqi <= 50:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<path d="M24 82 Q50 76 76 82 L76 114 Q50 120 24 114 Z" fill="#e879a0"/>
<ellipse cx="50" cy="112" rx="26" ry="14" fill="#c0537a"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#f4a261"/>
<circle cx="50" cy="54" r="24" fill="#f4a261"/>
<path d="M26 40 Q30 22 50 20 Q70 22 74 40 Q70 32 50 30 Q30 32 26 40 Z" fill="#8b1a4a"/>
<path d="M26 40 Q24 48 28 52" fill="#8b1a4a"/>
<path d="M74 40 Q76 48 72 52" fill="#8b1a4a"/>
<path d="M50 20 Q68 18 76 30 Q80 38 78 50 Q72 42 68 38" fill="#8b1a4a"/>
<circle cx="42" cy="50" r="3.5" fill="#1a1a1a"/>
<circle cx="58" cy="50" r="3.5" fill="#1a1a1a"/>
<circle cx="43.5" cy="48.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="48.5" r="1.5" fill="white"/>
<path d="M41 62 Q50 71 59 62" stroke="#c0392b" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<circle cx="37" cy="59" r="4" fill="rgba(255,150,100,0.3)"/>
<circle cx="63" cy="59" r="4" fill="rgba(255,150,100,0.3)"/>
<line x1="24" y1="90" x2="8" y2="74" stroke="#e879a0" stroke-width="7" stroke-linecap="round"/>
<line x1="76" y1="90" x2="92" y2="74" stroke="#e879a0" stroke-width="7" stroke-linecap="round"/>
<path d="M38 114 Q36 122 33 130" stroke="#c0537a" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M62 114 Q64 122 67 130" stroke="#c0537a" stroke-width="7" fill="none" stroke-linecap="round"/>
<circle cx="13" cy="55" r="3" fill="#68d391" opacity="0.8"/>
<circle cx="87" cy="46" r="2" fill="#68d391" opacity="0.6"/>
</svg>""", "#68d391", "Air is clean! Safe to go outside freely."

    elif aqi <= 100:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<path d="M24 82 Q50 76 76 82 L76 114 Q50 120 24 114 Z" fill="#9b5fc0"/>
<ellipse cx="50" cy="112" rx="26" ry="14" fill="#7b3fa0"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#f4a261"/>
<circle cx="50" cy="54" r="24" fill="#f4a261"/>
<path d="M26 40 Q30 22 50 20 Q70 22 74 40 Q70 32 50 30 Q30 32 26 40 Z" fill="#4a2070"/>
<path d="M26 40 Q24 48 28 52" fill="#4a2070"/>
<path d="M74 40 Q76 48 72 52" fill="#4a2070"/>
<ellipse cx="42" cy="50" rx="3.5" ry="3" fill="#1a1a1a"/>
<ellipse cx="58" cy="50" rx="3.5" ry="3" fill="#1a1a1a"/>
<circle cx="43.5" cy="48.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="48.5" r="1.5" fill="white"/>
<rect x="34" y="58" width="32" height="14" rx="7" fill="#c9b1ff" opacity="0.9"/>
<line x1="34" y1="65" x2="27" y2="63" stroke="#c9b1ff" stroke-width="2"/>
<line x1="66" y1="65" x2="73" y2="63" stroke="#c9b1ff" stroke-width="2"/>
<line x1="24" y1="92" x2="10" y2="80" stroke="#9b5fc0" stroke-width="7" stroke-linecap="round"/>
<line x1="76" y1="92" x2="90" y2="80" stroke="#9b5fc0" stroke-width="7" stroke-linecap="round"/>
<path d="M38 114 Q36 122 33 130" stroke="#7b3fa0" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M62 114 Q64 122 67 130" stroke="#7b3fa0" stroke-width="7" fill="none" stroke-linecap="round"/>
</svg>""", "#f6e05e", "Moderate air. Consider a light mask outside."

    elif aqi <= 200:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<path d="M24 82 Q50 76 76 82 L76 114 Q50 120 24 114 Z" fill="#b45309"/>
<ellipse cx="50" cy="112" rx="26" ry="14" fill="#92400e"/>
<rect x="44" y="68" width="12" height="16" rx="4" fill="#e8956d"/>
<circle cx="50" cy="54" r="24" fill="#e8956d"/>
<path d="M26 40 Q30 22 50 20 Q70 22 74 40 Q70 32 50 30 Q30 32 26 40 Z" fill="#1a1a2e"/>
<path d="M26 40 Q24 48 28 52" fill="#1a1a2e"/>
<path d="M74 40 Q76 48 72 52" fill="#1a1a2e"/>
<ellipse cx="42" cy="49" rx="4" ry="3" fill="#1a1a1a"/>
<ellipse cx="58" cy="49" rx="4" ry="3" fill="#1a1a1a"/>
<circle cx="43.5" cy="47.5" r="1.5" fill="white"/>
<circle cx="59.5" cy="47.5" r="1.5" fill="white"/>
<path d="M39 41 Q42 38 46 40" stroke="#3d2b1f" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M54 40 Q58 38 61 41" stroke="#3d2b1f" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M32 58 Q50 74 68 58 L68 70 Q50 84 32 70 Z" fill="#ddd"/>
<path d="M32 58 Q50 53 68 58" fill="#eee"/>
<line x1="32" y1="61" x2="24" y2="56" stroke="#bbb" stroke-width="2" stroke-linecap="round"/>
<line x1="68" y1="61" x2="76" y2="56" stroke="#bbb" stroke-width="2" stroke-linecap="round"/>
<line x1="24" y1="92" x2="10" y2="104" stroke="#b45309" stroke-width="7" stroke-linecap="round"/>
<line x1="76" y1="92" x2="90" y2="104" stroke="#b45309" stroke-width="7" stroke-linecap="round"/>
<path d="M38 114 Q36 122 33 130" stroke="#92400e" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M62 114 Q64 122 67 130" stroke="#92400e" stroke-width="7" fill="none" stroke-linecap="round"/>
<circle cx="10" cy="52" r="4" fill="#dd6b20" opacity="0.35"/>
<circle cx="88" cy="64" r="3" fill="#dd6b20" opacity="0.25"/>
</svg>""", "#fbd38d", "Poor air! Wear your N95 mask before stepping out."

    else:
        return """<svg class="char-svg" width="100" height="130" viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<path d="M22 80 Q50 74 78 80 L78 114 Q50 122 22 114 Z" fill="#8b2222"/>
<ellipse cx="50" cy="114" rx="28" ry="16" fill="#6b1a1a"/>
<ellipse cx="13" cy="110" rx="7" ry="5" fill="#a83232"/>
<ellipse cx="87" cy="110" rx="7" ry="5" fill="#a83232"/>
<rect x="43" y="67" width="14" height="15" rx="4" fill="#c0392b"/>
<circle cx="50" cy="52" r="26" fill="#c0392b"/>
<ellipse cx="50" cy="52" rx="18" ry="14" fill="#1a1a2e" opacity="0.85"/>
<ellipse cx="42" cy="49" rx="4.5" ry="3.5" fill="#ff6b6b" opacity="0.9"/>
<ellipse cx="58" cy="49" rx="4.5" ry="3.5" fill="#ff6b6b" opacity="0.9"/>
<circle cx="44" cy="47" r="2" fill="white" opacity="0.6"/>
<circle cx="60" cy="47" r="2" fill="white" opacity="0.6"/>
<path d="M24 40 Q50 25 76 40" stroke="#8b2222" stroke-width="4" fill="none"/>
<rect x="42" y="64" width="16" height="7" rx="3" fill="#555"/>
<rect x="46" y="67" width="8" height="2.5" rx="1.5" fill="#888"/>
<line x1="22" y1="90" x2="5" y2="74" stroke="#8b2222" stroke-width="9" stroke-linecap="round"/>
<line x1="78" y1="90" x2="95" y2="74" stroke="#8b2222" stroke-width="9" stroke-linecap="round"/>
<path d="M38 116 Q35 123 32 130" stroke="#6b1a1a" stroke-width="8" fill="none" stroke-linecap="round"/>
<path d="M62 116 Q65 123 68 130" stroke="#6b1a1a" stroke-width="8" fill="none" stroke-linecap="round"/>
<circle cx="8" cy="46" r="6" fill="#e53e3e" opacity="0.2"/>
<circle cx="92" cy="36" r="5" fill="#e53e3e" opacity="0.18"/>
</svg>""", "#fc8181", "HAZARDOUS! Stay indoors. Do not go outside without full protection."


# ── Hero ──────────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(
    f'<div class="hero-banner">'
    f'<div class="hero-sub">Real-Time Health Protection</div>'
    f'<div class="hero-title">Mumbai AQI Guardian</div>'
    f'<div class="hero-time">{now.strftime("%d %B %Y")} &nbsp;|&nbsp; {now.strftime("%I:%M %p")} &nbsp;|&nbsp; 24 &amp; 48 Hour Forecast</div>'
    f'</div>',
    unsafe_allow_html=True
)

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
st.markdown(
    '<div class="scale-wrap">'
    '<div class="scale-title">Air Quality Index - Reference Scale</div>'
    '<div class="scale-bar"></div>'
    '<div class="scale-labels"><span>0</span><span>50</span><span>100</span><span>200</span><span>300</span><span>400+</span></div>'
    '<div class="scale-chips">'
    '<span class="chip chip-green">0-50 Good</span>'
    '<span class="chip chip-yellow">51-100 Moderate</span>'
    '<span class="chip chip-orange">101-200 Poor</span>'
    '<span class="chip chip-red">201+ Danger</span>'
    '</div></div>',
    unsafe_allow_html=True
)

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

# Mini readouts — built with string concat, no triple-quotes, no HTML comments
mini_html = (
    '<div class="mini-grid">'
    '<div class="mini-card"><div class="mini-label">AQI Now</div>'
    f'<div class="mini-value">{current_aqi}<span class="mini-unit">AQI</span></div></div>'
    '<div class="mini-card"><div class="mini-label">PM2.5</div>'
    f'<div class="mini-value">{pm25:.1f}<span class="mini-unit">ug/m3</span></div></div>'
    '<div class="mini-card"><div class="mini-label">Temp</div>'
    f'<div class="mini-value">{temp:.1f}<span class="mini-unit">degC</span></div></div>'
    '<div class="mini-card"><div class="mini-label">Humidity</div>'
    f'<div class="mini-value">{humidity}<span class="mini-unit">%</span></div></div>'
    '<div class="mini-card"><div class="mini-label">Wind</div>'
    f'<div class="mini-value">{wind_speed:.1f}<span class="mini-unit">km/h</span></div></div>'
    '<div class="mini-card"><div class="mini-label">Season</div>'
    f'<div class="mini-value" style="font-size:0.9rem">{season}</div></div>'
    '</div>'
)
st.markdown(mini_html, unsafe_allow_html=True)

# ── Live character (BOY) based on current AQI ─────────────────────────────────
b_svg, char_color, char_tip = boy_svg(current_aqi)
r_now, _, _, _ = get_risk(current_aqi)
st.markdown(
    '<div class="character-wrap">'
    + b_svg +
    '<div class="character-text-block">'
    '<div class="character-label">Air Quality Status</div>'
    f'<div class="character-status" style="color:{char_color};">AQI: {current_aqi} - {r_now}</div>'
    f'<div class="character-tip">{char_tip}</div>'
    '</div></div>',
    unsafe_allow_html=True
)

# ── Predict Button ────────────────────────────────────────────────────────────
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

        # Alert banner
        if r24 in ["Very Poor", "Severe"] or r48 in ["Very Poor", "Severe"]:
            alert_cls, alert_msg = "alert-danger",  "HIGH ALERT - Dangerous air quality expected. Take immediate precautions."
        elif r24 == "Poor" or r48 == "Poor":
            alert_cls, alert_msg = "alert-warning", "CAUTION - Elevated AQI forecast. Sensitive groups should stay indoors."
        else:
            alert_cls, alert_msg = "alert-safe",    "CONDITIONS MANAGEABLE - Stay aware and monitor changes."
        st.markdown(f'<div class="alert-banner {alert_cls}">{alert_msg}</div>', unsafe_allow_html=True)

        # Forecast cards — BOY for 24h, GIRL for 48h
        st.markdown('<div class="section-label">Health Forecast</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")

        b24_svg, _, _ = boy_svg(pred_24)
        g48_svg, _, _ = girl_svg(pred_48)

        with c1:
            st.markdown(
                '<div class="pred-card pred-card-24">'
                '<div class="pred-hour">Next 24 Hours</div>'
                + b24_svg +
                f'<div class="pred-number" style="color:{c24};">{pred_24:.0f}</div>'
                f'<div class="pred-status" style="color:{c24};"><span class="dot {d24}"></span>{r24}</div>'
                '<div class="pred-badge">AQI Forecast</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                '<div class="pred-card pred-card-48">'
                '<div class="pred-hour">Next 48 Hours</div>'
                + g48_svg +
                f'<div class="pred-number" style="color:{c48};">{pred_48:.0f}</div>'
                f'<div class="pred-status" style="color:{c48};"><span class="dot {d48}"></span>{r48}</div>'
                '<div class="pred-badge">AQI Forecast</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # Health advice
        st.markdown('<div class="section-label">Personalised Health Advice</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="advice-card {cls24}">'
            f'<div class="advice-title" style="color:{c24};">24-Hour Outlook - {r24}</div>'
            f'<div class="advice-text">{get_health_advice(r24, "24 hours")}</div>'
            '</div>'
            f'<div class="advice-card {cls48}">'
            f'<div class="advice-title" style="color:{c48};">48-Hour Outlook - {r48}</div>'
            f'<div class="advice-text">{get_health_advice(r48, "48 hours")}</div>'
            '</div>',
            unsafe_allow_html=True
        )

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
