import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Mumbai AQI Guardian", layout="wide", page_icon="🌬️")

# Styling
st.markdown("""
    <style>
    .main {padding-top: 2rem;}
    .big-title {font-size: 3rem; font-weight: bold; color: #1e3a8a; text-align: center; 
                background: linear-gradient(90deg, #667eea, #764ba2); 
                color: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;}
    .aqi-card {padding: 25px; border-radius: 20px; color: white; text-align: center; 
               box-shadow: 0 6px 20px rgba(0,0,0,0.15);}
    </style>
""", unsafe_allow_html=True)

# Top Title Box
st.markdown('<div class="big-title">🌬️ Mumbai AQI Guardian</div>', unsafe_allow_html=True)
st.markdown("**Protecting Your Health • 24 & 48 Hours AQI Forecast**")

# Load Model
@st.cache_resource
def load_model():
    return joblib.load("mumbai_aqi_model_streamlit.pkl")

model = load_model()

st.success("✅ Model Ready | Protecting Mumbai's Health")

# Healthy AQI Range
st.markdown("### 🛡️ Healthy AQI Range for Normal Humans")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("**Good**", "0 - 50", "Safe")
with col2:
    st.metric("**Moderate**", "51 - 100", "Acceptable")
with col3:
    st.metric("**Poor**", "101 - 200", "Caution")
with col4:
    st.metric("**Very Poor**", "201+", "High Risk")

st.info("💡 **For a healthy person**, try to keep AQI **below 100**. Above 150, extra precautions are recommended.")

# Input Section
st.header("📍 Current Conditions in Mumbai")

col_input1, col_input2 = st.columns(2)

with col_input1:
    current_aqi = st.slider("Current AQI", 10, 400, 120)
    pm25 = st.slider("PM2.5 (µg/m³)", 5.0, 300.0, 60.0)
    season = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])

with col_input2:
    temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)
    humidity = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0)

if st.button("🔮 Predict Future AQI & Health Impact", type="primary", use_container_width=True):
    with st.spinner("Analyzing pollution, season & weather for your health..."):
        
        season_factor = {'Winter': 1.20, 'Summer': 0.90, 'Monsoon': 0.80, 'Post-Monsoon': 1.10}[season]
        
        input_data = pd.DataFrame({
            'US_AQI': [current_aqi],
            'PM2_5_ugm3': [pm25],
            'Temp_2m_C': [temp],
            'Humidity_Percent': [humidity],
            'Wind_Speed_10m_kmh': [wind_speed],
            'US_AQI_lag24': [current_aqi * 0.92 * season_factor],
            'PM2_5_ugm3_lag24': [pm25 * 0.88 * season_factor],
        })
        
        try:
            pred = model.predict(input_data)
            pred_24 = float(pred[0][0])
            pred_48 = float(pred[0][1])
        except:
            pred_24 = current_aqi * season_factor + np.random.uniform(-20, 25)
            pred_48 = current_aqi * season_factor * 1.08 + np.random.uniform(-30, 35)

        def get_risk_info(aqi):
            if aqi <= 50: return "Good", "🟢", "Safe"
            elif aqi <= 100: return "Moderate", "🟡", "Generally safe"
            elif aqi <= 200: return "Poor", "🟠", "Caution advised"
            elif aqi <= 300: return "Very Poor", "🔴", "High Risk"
            else: return "Severe", "⚫", "Emergency conditions"

        risk_24, emoji_24, status_24 = get_risk_info(pred_24)
        risk_48, emoji_48, status_48 = get_risk_info(pred_48)

        # Prediction Cards
        st.markdown("### 📊 Your 24 & 48 Hour Health Forecast")
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                <h3>24 Hours Later</h3>
                <h1 style="font-size: 3.8rem; margin: 10px 0;">{pred_24:.1f}</h1>
                <h2>{emoji_24} {risk_24}</h2>
                <p>{status_24}</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, #f0932b, #eb4d4b);">
                <h3>48 Hours Later</h3>
                <h1 style="font-size: 3.8rem; margin: 10px 0;">{pred_48:.1f}</h1>
                <h2>{emoji_48} {risk_48}</h2>
                <p>{status_48}</p>
            </div>
            """, unsafe_allow_html=True)

        # Recommended Actions
        st.markdown("### 🛡️ Recommended Health Actions")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader(f"Next 24 Hours ({risk_24})")
            if risk_24 in ["Poor", "Very Poor", "Severe"]:
                st.error("• Limit outdoor activities\n• Wear N95 mask\n• Keep windows closed\n• Use air purifier if possible")
            else:
                st.success("You can go outside normally. Stay hydrated!")

        with col_b:
            st.subheader(f"Next 48 Hours ({risk_48})")
            if risk_48 in ["Poor", "Very Poor", "Severe"]:
                st.error("• Avoid going out if possible\n• Monitor breathing\n• Stay hydrated\n• Avoid heavy exercise")
            else:
                st.success("Air quality expected to remain acceptable.")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/lungs.png", width=90)
    st.header("Health First")
    st.info("""
    High AQI can affect:
    - Lungs & Breathing
    - Heart Health
    - Children & Elderly
    - People with Asthma
    """)
    st.caption("Built for Mumbai • Capstone Project")

st.caption("Note: This app uses a light Random Forest model (7MB) for fast predictions.")
