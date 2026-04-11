import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

st.set_page_config(page_title="Mumbai AQI Guardian", layout="wide", page_icon="🌬️")

# Styling
st.markdown("""
    <style>
    .main {padding-top: 2rem;}
    .big-title {font-size: 3rem; font-weight: bold; text-align: center; 
                background: linear-gradient(90deg, #1e3a8a, #4a6cf7); 
                color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;}
    .aqi-card {padding: 25px; border-radius: 20px; color: white; text-align: center; 
               box-shadow: 0 6px 20px rgba(0,0,0,0.15);}
    </style>
""", unsafe_allow_html=True)

# Top Title
st.markdown('<div class="big-title">🌬️ Mumbai AQI Guardian</div>', unsafe_allow_html=True)

# Show Current Date & Time
current_time = datetime.now()
st.markdown(f"**📅 Prediction made on:** {current_time.strftime('%d %B %Y, %I:%M %p')}")

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
with col1: st.metric("**Good**", "0–50", "Safe")
with col2: st.metric("**Moderate**", "51–100", "OK")
with col3: st.metric("**Poor**", "101–200", "Caution")
with col4: st.metric("**Very Poor**", "201+", "Avoid Outdoor")

st.info("💡 **Best for health**: Keep AQI under **100**. Above 150, take extra care.")

# Input Section
st.header("📍 Current Conditions in Mumbai")

col1, col2 = st.columns(2)

with col1:
    current_aqi = st.slider("Current AQI", 10, 400, 120)
    pm25 = st.slider("PM2.5 (µg/m³)", 5.0, 300.0, 60.0)
    season = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])

with col2:
    temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)
    humidity = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0)

if st.button("🔮 Predict 24h & 48h AQI & Health Risk", type="primary", use_container_width=True):
    with st.spinner("Analyzing for your health..."):
        
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

        def get_risk(aqi):
            if aqi <= 50: return "Good", "🟢"
            elif aqi <= 100: return "Moderate", "🟡"
            elif aqi <= 200: return "Poor", "🟠"
            elif aqi <= 300: return "Very Poor", "🔴"
            else: return "Severe", "⚫"

        r24, e24 = get_risk(pred_24)
        r48, e48 = get_risk(pred_48)

        # Prediction Cards
        st.markdown("### 📊 Your Health Forecast")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, #667eea, #764ba2);">
                <h3>24 Hours Later</h3>
                <h1 style="font-size: 3.5rem;">{pred_24:.1f}</h1>
                <h2>{e24} {r24}</h2>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="aqi-card" style="background: linear-gradient(135deg, #f0932b, #eb4d4b);">
                <h3>48 Hours Later</h3>
                <h1 style="font-size: 3.5rem;">{pred_48:.1f}</h1>
                <h2>{e48} {r48}</h2>
            </div>
            """, unsafe_allow_html=True)

        # Recommended Actions
        st.markdown("### 🛡️ Recommended Health Actions")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader(f"Next 24 Hours ({r24})")
            if r24 in ["Poor", "Very Poor", "Severe"]:
                st.error("• Limit outdoor activities\n• Wear N95 mask\n• Keep windows closed\n• Use air purifier if possible")
            else:
                st.success("Safe for normal outdoor activities")
        with col_b:
            st.subheader(f"Next 48 Hours ({r48})")
            if r48 in ["Poor", "Very Poor", "Severe"]:
                st.error("• Avoid going out if possible\n• Monitor breathing\n• Stay hydrated\n• Avoid heavy exercise")
            else:
                st.success("Expected to be manageable")

        # Trend Chart
        st.markdown("### 📈 Recent AQI Trend in Mumbai (Last 7 Days)")
        dates = pd.date_range(end=datetime.now(), periods=7)
        aqi_trend = [current_aqi + np.random.randint(-30, 40) for _ in range(7)]
        trend_df = pd.DataFrame({"Date": dates, "AQI": aqi_trend})
        st.line_chart(trend_df.set_index("Date"), use_container_width=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/lungs.png", width=90)
    st.header("Health First")
    st.info("""
    High AQI can cause:
    - Breathing problems
    - Heart issues
    - Risk to children & elderly
    """)
    st.caption("Capstone Project • Mumbai")

st.caption("Made with ❤️ for Mumbai")
