# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import random
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mumbai AQI Guardian",
    layout="wide",
    page_icon="🌬️",
    initial_sidebar_state="collapsed"
)

# Custom CSS for UI and Hiding Streamlit Branding
st.markdown("""
    <style>
    /* Hide Streamlit Header, Footer, and Toolbar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Background and global styles */
    .main { background-color: #0e1117; color: #ffffff; padding-top: 1rem; }
    
    /* Mobile-first card container */
    .aqi-card {
        background: #1e2130;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #3d4156;
        text-align: center;
    }
    
    /* Character Animation Container */
    .char-container {
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
    }

    /* Fixed Markdown Symbol Fixes (Using standard text/HTML) */
    .unit-text { font-size: 0.8rem; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# Helper function for Character SVG (Boy and Girl)
def get_character_svg(aqi_level, gender="boy"):
    # Gender details
    hair_color = "#4A3728" if gender == "boy" else "#FFD700"
    hair_style = '<rect x="35" y="25" width="30" height="15" fill="#4A3728"/>' if gender == "boy" else '<path d="M30 25 Q50 10 70 25 L75 50 Q50 40 25 50 Z" fill="#FFD700"/>'
    
    # AQI Logic for protection
    color = "#00E400" # Good
    mask = ""
    expression = '<path d="M40 55 Q50 65 60 55" stroke="white" fill="none" stroke-width="2"/>' # Smile
    
    if aqi_level > 50: # Moderate
        color = "#FFFF00"
        mask = '<rect x="40" y="52" width="20" height="10" rx="2" fill="#ADD8E6" opacity="0.8"/>'
    if aqi_level > 100: # Poor
        color = "#FF7E00"
        mask = '<path d="M38 50 L62 50 L58 65 L42 65 Z" fill="#FFFFFF"/>' # N95 Mask
        expression = ""
    if aqi_level > 200: # Danger
        color = "#FF0000"
        mask = '<circle cx="50" cy="58" r="12" fill="#333" stroke="white"/>' # Respirator
        expression = ""

    svg = f"""
    <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="45" fill="{color}" opacity="0.1"/>
        {hair_style}
        <circle cx="50" cy="45" r="20" fill="#FFDBAC"/>
        <circle cx="43" cy="42" r="2" fill="black"/>
        <circle cx="57" cy="42" r="2" fill="black"/>
        {expression}
        {mask}
    </svg>
    """
    return svg

# --- APP LAYOUT ---
st.title("🌬️ Mumbai AQI Guardian")

# Simulating Model Prediction for UI display
aqi_val = st.slider("Select Current AQI for Preview", 0, 300, 85)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="aqi-card">', unsafe_allow_html=True)
    st.subheader("24h Forecast")
    # Randomly pick Girl for 24h
    st.markdown(f'<div class="char-container">{get_character_svg(aqi_val, "girl")}</div>', unsafe_allow_html=True)
    st.metric("Predicted AQI", f"{aqi_val + 10}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="aqi-card">', unsafe_allow_html=True)
    st.subheader("48h Forecast")
    # Randomly pick Boy for 48h
    st.markdown(f'<div class="char-container">{get_character_svg(aqi_val + 20, "boy")}</div>', unsafe_allow_html=True)
    st.metric("Predicted AQI", f"{aqi_val + 25}")
    st.markdown('</div>', unsafe_allow_html=True)

# Guide on fixing markdown bugs
with st.expander("🛠️ How to fix Markdown Bugs (Developer Guide)"):
    st.write("""
    The "symbols" (like ðŸ) appear because of **UTF-8 encoding mismatches** between your code and the server.
    
    **How to prevent this:**
    1. **Avoid Emojis in HTML strings:** Use standard icons or SVG code instead.
    2. **Avoid Special Symbols:** Replace `°C` with `deg C` and `µg/m³` with `ug/m3` inside `st.markdown` blocks.
    3. **Save as UTF-8:** Always ensure your text editor saves the `.py` file with **UTF-8 encoding**.
    """)
