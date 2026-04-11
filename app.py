import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Mumbai AQI Predictor", layout="wide")

st.title("🌬️ Mumbai Air Quality Predictor")
st.markdown("**24 & 48 Hours AQI Forecast with Early Warnings**")

# Load model
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

# ====================== MAIN APP ======================
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
        
        # Create a DataFrame with ALL expected features (filled with reasonable defaults)
        feature_names = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else None
        
        if feature_names is not None:
            input_data = pd.DataFrame(0, index=[0], columns=feature_names)
            
            # Fill the important features we have from user input
            input_data['US_AQI'] = current_aqi
            input_data['PM2_5_ugm3'] = pm25
            input_data['Temp_2m_C'] = temp
            input_data['Humidity_Percent'] = humidity
            input_data['Wind_Speed_10m_kmh'] = wind_speed
            
            # Add some lag features with logical values
            input_data['US_AQI_lag24'] = current_aqi * 0.95
            input_data['PM2_5_ugm3_lag24'] = pm25 * 0.92
            input_data['US_AQI_lag1'] = current_aqi
            input_data['PM2_5_ugm3_lag1'] = pm25
            
        else:
            # Fallback if feature names not available
            input_data = pd.DataFrame({
                'US
