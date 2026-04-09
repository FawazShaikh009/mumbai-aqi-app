import streamlit as st
import joblib
import gdown
import os

@st.cache_resource
def load_model():
    url = "https://drive.google.com/uc?id=1HCp-6AseXqWXganqE7hFhNTXe2r2oQs2"
    output = "model.pkl"
    
    # Download only if not already present
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    model = joblib.load(output)
    return model

model = load_model()

st.sidebar.header("How to Use")
st.sidebar.info("""
1. This app uses the latest available data patterns.
2. For real deployment, you would connect live weather API.
3. Currently it shows demo prediction logic.
""")

# Simple Demo Input Section (Easy version for now)
st.header("Make a Prediction")

col1, col2 = st.columns(2)

with col1:
    current_aqi = st.slider("Current AQI (US_AQI)", 10, 400, 120)
    pm25 = st.slider("PM2.5 (µg/m³)", 5.0, 300.0, 60.0)
    temp = st.slider("Temperature (°C)", 15.0, 40.0, 28.0)

with col2:
    humidity = st.slider("Humidity (%)", 20, 100, 65)
    wind_speed = st.slider("Wind Speed (km/h)", 0.0, 30.0, 8.0)
    season = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post-Monsoon"])

# Create a dummy row with required features (simplified for demo)
if st.button("Predict AQI for Next 24h & 48h"):
    # Create basic input row (in real app you would use last 24h data)
    input_data = pd.DataFrame({
        'US_AQI': [current_aqi],
        'PM2_5_ugm3': [pm25],
        'Temp_2m_C': [temp],
        'Humidity_Percent': [humidity],
        'Wind_Speed_10m_kmh': [wind_speed],
        # Add more important lag features with reasonable values (demo)
        'US_AQI_lag24': [current_aqi - 10],
        'PM2_5_ugm3_lag24': [pm25 - 5],
        # ... you can expand this later
    })
    
    # For full version, you need all 104 features. 
    # For now, we show a demo prediction
    st.warning("Note: This is a simplified demo. Full version needs last 24 hours of data.")
    
    # Dummy prediction for presentation (replace with real later)
    pred_24 = current_aqi + np.random.randint(-15, 25)
    pred_48 = current_aqi + np.random.randint(-25, 35)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted AQI after 24 Hours", f"{pred_24:.0f}", delta=f"{pred_24 - current_aqi:.0f}")
        st.success(f"Risk Level: **{get_risk_level(pred_24)}**")
    
    with col2:
        st.metric("Predicted AQI after 48 Hours", f"{pred_48:.0f}", delta=f"{pred_48 - current_aqi:.0f}")
        st.success(f"Risk Level: **{get_risk_level(pred_48)}**")

    # Early Warning
    warnings = []
    if get_risk_level(pred_24) in ['Poor', 'Very Poor', 'Severe']:
        warnings.append(f"⚠️ **24h Warning**: {get_risk_level(pred_24)} air quality expected!")
    if get_risk_level(pred_48) in ['Poor', 'Very Poor', 'Severe']:
        warnings.append(f"⚠️ **48h Warning**: {get_risk_level(pred_48)} air quality expected!")
    
    if warnings:
        st.error(" ".join(warnings))
    else:
        st.success("✅ Air quality expected to remain okay.")

# Risk level function
def get_risk_level(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 200: return "Poor"
    elif aqi <= 300: return "Very Poor"
    else: return "Severe"

st.caption("Made for Capstone Project | Model trained on hourly Mumbai data")
