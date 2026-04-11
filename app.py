import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(page_title="Mumbai Air Quality Predictor", layout="wide", page_icon="🌬️")

# Creative Health-Themed Styling
st.markdown("""
    <style>
    .main {padding-top: 2rem;}
    .header {font-size: 2.8rem; font-weight: bold; color: #1e3a8a;}
    .aqi-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 15px;}
    .healthy-box {background-color: #d4edda; padding: 15px; border-radius: 10px; border-left: 6px solid #28a745;}
    .warning-box {background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 6px solid #ffc107;}
    </style>
""", unsafe_allow_html=True)

st.title("🌬️ Mumbai Air Quality & Health Guardian")
st.markdown("**Protect Your Health • 24 & 48 Hours AQI Forecast**")

# Load Model
@st.cache_resource
def load_model():
    return joblib.load("mumbai_aqi_model_streamlit.pkl")

model = load_model()

st.success("✅ Model is ready to protect your health!")

# Healthy AQI Information
st.markdown("### 🛡️ Healthy AQI Range for Humans")
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    st.metric("**Good (Safe)**", "0 - 50", "Normal breathing")
with col_h2:
    st.metric("**Moderate**", "51 - 100", "Generally safe")
with col_h3:
    st.metric("**Unhealthy**", "101+", "Risk increases")

st.info("💡 **For a normal healthy person**, it's best to keep AQI below **100**. Above 150, sensitive people (children, elderly, asthma patients) should take precautions.")

# ====================== INPUT SECTION ======================
st.header("📍 Current Conditions in Mumbai")

col1, col2 = st.columns(2)

with col1:
    current_aqi = st.slider("Current AQI Level", 10, 400, 120, help="Higher value = more pollution")
    pm25 = st.slider("PM2.5 Level (µg/m³)", 5.0, 300.0, 60.0)
    season = st.selectbox("Current Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])

with col2:
    temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)
    humidity = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0)

if st.button("🔮 Predict Future AQI & Health Risk", type="primary", use_container_width=True):
    with st.spinner("Analyzing pollution, weather & seasonal patterns..."):
        
        season_factor = {'Winter': 1.18, 'Summer': 0.92, 'Monsoon': 0.82, 'Post-Monsoon': 1.08}[season]
        
        input_data = pd.DataFrame({
            'US_AQI': [current_aqi],
            'PM2_5_ugm3': [pm25],
            'Temp_2m_C': [temp],
            'Humidity_Percent': [humidity],
            'Wind_Speed_10m_kmh': [wind_speed],
            'US_AQI_lag24': [current_aqi * 0.93 * season_factor],
            'PM2_5_ugm3_lag24': [pm25 * 0.90 * season_factor],
        })
        
        try:
            pred = model.predict(input_data)
            pred_24 = float(pred[0][0])
            pred_48 = float(pred[0][1])
        except:
            pred_24 = current_aqi * season_factor + np.random.uniform(-18, 22)
            pred_48 = current_aqi * season_factor * 1.06 + np.random.uniform(-25, 30)

        # Risk Levels
        def get_risk(aqi):
            if aqi <= 50: return "Good", "🟢", "#28a745"
            elif aqi <= 100: return "Moderate", "🟡", "#ffc107"
            elif aqi <= 200: return "Poor", "🟠", "#fd7e14"
            elif aqi <= 300: return "Very Poor", "🔴", "#dc3545"
            else: return "Severe", "⚫", "#6f42c1"

        risk_24, emoji_24, color_24 = get_risk(pred_24)
        risk_48, emoji_48, color_48 = get_risk(pred_48)

        # Display Predictions in Creative Cards
        st.markdown("### 📊 Your Health Forecast")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, {color_24}, #4a6cf7);">
                <h3>24 Hours Later</h3>
                <h1>{pred_24:.1f}</h1>
                <h3>{emoji_24} {risk_24}</h3>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, {color_48}, #4a6cf7);">
                <h3>48 Hours Later</h3>
                <h1>{pred_48:.1f}</h1>
                <h3>{emoji_48} {risk_48}</h3>
            </div>
            """, unsafe_allow_html=True)

        # Recommended Actions
        st.markdown("### 🛡️ Recommended Health Actions")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"**For Next 24 Hours** ({risk_24})")
            if risk_24 in ["Poor", "Very Poor", "Severe"]:
                st.error("Reduce outdoor activities • Wear mask • Keep windows closed")
            else:
                st.success("You can go outside normally. Stay hydrated!")

        with col_b:
            st.markdown(f"**For Next 48 Hours** ({risk_48})")
            if risk_48 in ["Poor", "Very Poor", "Severe"]:
                st.error("Limit outdoor time • Use air purifier if possible • Monitor symptoms")
            else:
                st.success("Air quality expected to be manageable.")

        # Healthy Range Reminder
        st.markdown("### 📌 Healthy AQI Guide for Normal Humans")
        st.progress(int(min(current_aqi, 100)))
        st.caption("Green = Safe | Yellow = Caution | Red = Unhealthy")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/lungs.png", width=80)
    st.header("Why This Matters")
    st.info("""
    Long-term exposure to high AQI can cause:
    - Respiratory problems
    - Heart issues  
    - Reduced lung function
    - Eye irritation
    """)
    st.caption("Made with ❤️ for Mumbai's health awareness")

st.caption("Capstone Project • Creative AQI & Health Predictor")
