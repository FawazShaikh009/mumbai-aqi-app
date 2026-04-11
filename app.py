import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Mumbai AQI Predictor", layout="wide")

st.title("🌬️ Mumbai Air Quality Predictor")
st.markdown("**24 & 48 Hours AQI Forecast with Early Warnings**")

# Load the model (now directly from GitHub)
@st.cache_resource
def load_model():
    model = joblib.load("mumbai_aqi_model_streamlit.pkl")
    return model

model = load_model()
st.success("✅ Model loaded successfully!")

# Risk Level Function
def get_risk_level(aqi):
    if aqi <= 50:   return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 200: return "Poor"
    elif aqi <= 300: return "Very Poor"
    else:           return "Severe"

# Input Section
st.header("Enter Current Conditions")

col1, col2 = st.columns(2)

with col1:
    current_aqi = st.slider("Current AQI", 10, 400, 120)
    pm25 = st.slider("PM2.5 (µg/m³)", 5.0, 300.0, 60.0)
    temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)

with col2:
    humidity = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0)

if st.button("🔮 Predict 24h & 48h AQI", type="primary"):
    with st.spinner("Predicting..."):
        input_df = pd.DataFrame({
            'US_AQI': [current_aqi],
            'PM2_5_ugm3': [pm25],
            'Temp_2m_C': [temp],
            'Humidity_Percent': [humidity],
            'Wind_Speed_10m_kmh': [wind_speed],
            'US_AQI_lag24': [current_aqi - 8],
            'PM2_5_ugm3_lag24': [pm25 - 5],
        })
        
        pred = model.predict(input_df)
        pred_24 = pred[0][0]
        pred_48 = pred[0][1]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("**24 Hours Later**", f"{pred_24:.1f}", f"{pred_24 - current_aqi:+.1f}")
            st.success(f"Risk: **{get_risk_level(pred_24)}**")
        
        with c2:
            st.metric("**48 Hours Later**", f"{pred_48:.1f}", f"{pred_48 - current_aqi:+.1f}")
            st.success(f"Risk: **{get_risk_level(pred_48)}**")
        
        if get_risk_level(pred_24) in ["Poor", "Very Poor", "Severe"]:
            st.error(f"⚠️ 24h: {get_risk_level(pred_24)} air quality expected!")
        if get_risk_level(pred_48) in ["Poor", "Very Poor", "Severe"]:
            st.error(f"⚠️ 48h: {get_risk_level(pred_48)} air quality expected!")

st.caption("Capstone Project • Random Forest • Mumbai AQI 24-48h Prediction")
