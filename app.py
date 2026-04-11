import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Mumbai AQI Predictor", layout="wide")

st.title("🌬️ Mumbai Air Quality Predictor")
st.markdown("**24 & 48 Hours AQI Forecast with Early Warnings**")

# ====================== LOAD MODEL ======================
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

# ====================== INPUT SECTION ======================
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
    with st.spinner("Making prediction..."):
        
        # Create input with all expected features (safe way)
        input_data = pd.DataFrame(0.0, index=[0], columns=model.feature_names_in_)
        
        # Fill known important features
        input_data['US_AQI'] = current_aqi
        if 'PM2_5_ugm3' in input_data.columns:
            input_data['PM2_5_ugm3'] = pm25
        if 'Temp_2m_C' in input_data.columns:
            input_data['Temp_2m_C'] = temp
        if 'Humidity_Percent' in input_data.columns:
            input_data['Humidity_Percent'] = humidity
        if 'Wind_Speed_10m_kmh' in input_data.columns:
            input_data['Wind_Speed_10m_kmh'] = wind_speed
        
        # Add some lag features
        if 'US_AQI_lag24' in input_data.columns:
            input_data['US_AQI_lag24'] = current_aqi * 0.95
        if 'PM2_5_ugm3_lag24' in input_data.columns:
            input_data['PM2_5_ugm3_lag24'] = pm25 * 0.92
        if 'US_AQI_lag1' in input_data.columns:
            input_data['US_AQI_lag1'] = current_aqi
        if 'PM2_5_ugm3_lag1' in input_data.columns:
            input_data['PM2_5_ugm3_lag1'] = pm25
        
        # Make prediction
        pred = model.predict(input_data)
        pred_24 = pred[0][0]
        pred_48 = pred[0][1]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("**24 Hours Later**", f"{pred_24:.1f}", f"{pred_24 - current_aqi:+.1f}")
            st.success(f"Risk: **{get_risk_level(pred_24)}**")
        
        with c2:
            st.metric("**48 Hours Later**", f"{pred_48:.1f}", f"{pred_48 - current_aqi:+.1f}")
            st.success(f"Risk: **{get_risk_level(pred_48)}**")
        
        # Early Warnings
        if get_risk_level(pred_24) in ["Poor", "Very Poor", "Severe"]:
            st.error(f"⚠️ 24h Warning: {get_risk_level(pred_24)} air quality expected!")
        if get_risk_level(pred_48) in ["Poor", "Very Poor", "Severe"]:
            st.error(f"⚠️ 48h Warning: {get_risk_level(pred_48)} air quality expected!")

st.caption("Capstone Project • Random Forest Model • Mumbai AQI Prediction")
