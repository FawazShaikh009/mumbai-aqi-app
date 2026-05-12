"""
India AQI Predictor — Streamlit App
Upgraded from Mumbai-only to all 29 Indian cities.

Files needed in the same folder as this script:
  - india_aqi_model_streamlit.pkl   (trained model)
  - india_model_features.pkl         (feature names list from notebook)
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India AQI Predictor",
    page_icon="🇮🇳",
    layout="wide",
)

# ── Constants ──────────────────────────────────────────────────────────────────
CITIES = [
    'Agartala', 'Ahmedabad', 'Aizawl', 'Bengaluru', 'Bhopal',
    'Bhubaneswar', 'Chandigarh', 'Chennai', 'Dehradun', 'Delhi',
    'Gangtok', 'Gurugram', 'Guwahati', 'Hyderabad', 'Imphal',
    'Itanagar', 'Jaipur', 'Kohima', 'Kolkata', 'Lucknow',
    'Mumbai', 'Panaji', 'Patna', 'Raipur', 'Ranchi',
    'Shillong', 'Shimla', 'Thiruvananthapuram', 'Visakhapatnam'
]

CITY_STATES = {
    'Agartala': 'Tripura', 'Ahmedabad': 'Gujarat', 'Aizawl': 'Mizoram',
    'Bengaluru': 'Karnataka', 'Bhopal': 'Madhya Pradesh',
    'Bhubaneswar': 'Odisha', 'Chandigarh': 'Chandigarh',
    'Chennai': 'Tamil Nadu', 'Dehradun': 'Uttarakhand', 'Delhi': 'Delhi',
    'Gangtok': 'Sikkim', 'Gurugram': 'Haryana', 'Guwahati': 'Assam',
    'Hyderabad': 'Telangana', 'Imphal': 'Manipur', 'Itanagar': 'Arunachal Pradesh',
    'Jaipur': 'Rajasthan', 'Kohima': 'Nagaland', 'Kolkata': 'West Bengal',
    'Lucknow': 'Uttar Pradesh', 'Mumbai': 'Maharashtra', 'Panaji': 'Goa',
    'Patna': 'Bihar', 'Raipur': 'Chhattisgarh', 'Ranchi': 'Jharkhand',
    'Shillong': 'Meghalaya', 'Shimla': 'Himachal Pradesh',
    'Thiruvananthapuram': 'Kerala', 'Visakhapatnam': 'Andhra Pradesh'
}

AQI_LEVELS = {
    "Good":      (0,   50,  "#00e400", "😊 Air quality is satisfactory. Outdoor activities are fine."),
    "Moderate":  (51,  100, "#ffff00", "😐 Acceptable air quality. Sensitive people should limit prolonged outdoor exertion."),
    "Poor":      (101, 200, "#ff7e00", "😷 Unhealthy for sensitive groups. Reduce prolonged outdoor exertion."),
    "Very Poor": (201, 300, "#ff0000", "🚨 Unhealthy. Everyone should reduce outdoor exertion."),
    "Severe":    (301, 999, "#7e0023", "☠️ Hazardous! Avoid all outdoor activity."),
}

def get_risk_level(aqi):
    if aqi <= 50:   return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 200: return "Poor"
    elif aqi <= 300: return "Very Poor"
    else:            return "Severe"

# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model    = joblib.load("india_aqi_model_streamlit.pkl")
    features = joblib.load("india_model_features.pkl")
    return model, features

try:
    model, FEATURES = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🇮🇳 India AQI Predictor")
st.markdown("Predict **24-hour and 48-hour Air Quality Index** for 29 Indian cities.")
st.divider()

# ── Sidebar inputs ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📍 Location & Time")
    city = st.selectbox("Select City", CITIES, index=CITIES.index("Mumbai"))
    state = CITY_STATES[city]
    st.caption(f"State: **{state}**")

    st.divider()
    st.header("🌤️ Weather Conditions")

    col1, col2 = st.columns(2)
    with col1:
        temp     = st.number_input("Temperature (°C)", -5.0, 50.0, 28.0, 0.5)
        humidity = st.number_input("Humidity (%)", 0, 100, 65)
        wind_spd = st.number_input("Wind Speed (km/h)", 0.0, 100.0, 12.0, 0.5)
    with col2:
        pressure = st.number_input("Pressure (hPa)", 950.0, 1050.0, 1010.0, 0.5)
        dew_pt   = st.number_input("Dew Point (°C)", -10.0, 40.0, 20.0, 0.5)
        precip   = st.number_input("Precipitation (mm)", 0.0, 200.0, 0.0, 0.5)

    wind_dir = st.slider("Wind Direction (°)", 0, 360, 180)

    st.divider()
    st.header("💨 Current Pollutants")
    col3, col4 = st.columns(2)
    with col3:
        pm25 = st.number_input("PM2.5 (µg/m³)", 0.0, 500.0, 35.0, 1.0)
        pm10 = st.number_input("PM10 (µg/m³)", 0.0, 600.0, 55.0, 1.0)
        no2  = st.number_input("NO₂ (µg/m³)", 0.0, 200.0, 20.0, 1.0)
    with col4:
        o3   = st.number_input("O₃ (µg/m³)", 0.0, 300.0, 40.0, 1.0)
        so2  = st.number_input("SO₂ (µg/m³)", 0.0, 100.0, 8.0, 0.5)
        co   = st.number_input("CO (µg/m³)", 0.0, 10000.0, 200.0, 10.0)

    current_aqi = st.number_input("Current AQI (US)", 0, 500, 80)

    st.divider()
    st.header("📅 Date & Time Context")
    month   = st.selectbox("Month", range(1, 13), index=10,
                            format_func=lambda m: ['Jan','Feb','Mar','Apr','May','Jun',
                                                    'Jul','Aug','Sep','Oct','Nov','Dec'][m-1])
    hour    = st.slider("Hour of Day", 0, 23, 12)
    season  = st.selectbox("Season", ["Winter", "Summer", "Monsoon", "Post_Monsoon"])
    is_weekend   = st.checkbox("Is Weekend?", False)
    festival     = st.checkbox("Festival Period?", False)
    crop_burning = st.checkbox("Crop Burning Season?", False)

    predict_btn = st.button("🔮 Predict AQI", type="primary", use_container_width=True)

# ── Main panel ─────────────────────────────────────────────────────────────────
if not model_loaded:
    st.error("""
    ⚠️ **Model files not found!**

    Please place these two files in the same folder as `streamlit_app.py`:
    - `india_aqi_model_streamlit.pkl`
    - `india_model_features.pkl`

    You can generate them by running the notebook: `India_AQI_Predictor_AllCities.ipynb`
    """)
    st.stop()

if predict_btn:
    # ── Build input row ──────────────────────────────────────────────────────
    # Start with zeros for all features
    input_data = {f: 0 for f in FEATURES}

    # Numeric features
    numeric_map = {
        'Temp_2m_C': temp, 'Humidity_Percent': humidity,
        'Wind_Speed_10m_kmh': wind_spd, 'Wind_Dir_10m': wind_dir,
        'Pressure_MSL_hPa': pressure, 'Surface_Pressure_hPa': pressure - 1.5,
        'Dew_Point_C': dew_pt, 'Precipitation_mm': precip, 'Rain_mm': precip,
        'PM2_5_ugm3': pm25, 'PM10_ugm3': pm10, 'PM_Ratio': pm25 / max(pm10, 1),
        'NO2_ugm3': no2, 'O3_ugm3': o3, 'SO2_ugm3': so2, 'CO_ugm3': co,
        'US_AQI': current_aqi,
        'Month': month, 'Hour': hour,
        'Is_Weekend': int(is_weekend),
        'Festival_Period': int(festival),
        'Crop_Burning_Season': int(crop_burning),
        'Is_Raining': int(precip > 0), 'Heavy_Rain': int(precip > 20),
    }
    for k, v in numeric_map.items():
        if k in input_data:
            input_data[k] = v

    # Lag features — assume steady state (current values) for simplicity
    lag_cols_base = ['US_AQI', 'PM2_5_ugm3', 'PM10_ugm3', 'NO2_ugm3', 'O3_ugm3',
                     'Temp_2m_C', 'Humidity_Percent', 'Wind_Speed_10m_kmh']
    lag_vals      = [current_aqi, pm25, pm10, no2, o3, temp, humidity, wind_spd]
    for base, val in zip(lag_cols_base, lag_vals):
        for lag in [1, 3, 6, 12, 24]:
            key = f'{base}_lag{lag}'
            if key in input_data:
                input_data[key] = val

    # One-hot encode City (drop_first=True means first city alphabetically has no dummy)
    all_cities_sorted = sorted(CITIES)
    ref_city = all_cities_sorted[0]  # 'Agartala' is reference (no dummy column)
    if city != ref_city:
        city_col = f'City_{city}'
        if city_col in input_data:
            input_data[city_col] = 1

    # One-hot encode State
    all_states_sorted = sorted(set(CITY_STATES.values()))
    ref_state = all_states_sorted[0]
    if state != ref_state:
        state_col = f'State_{state}'
        if state_col in input_data:
            input_data[state_col] = 1

    # One-hot encode Season
    for s in ["Post_Monsoon", "Summer", "Winter"]:  # Monsoon is reference
        col = f'Season_{s}'
        if col in input_data:
            input_data[col] = int(season == s)

    # Time of Day
    if 6 <= hour < 12:   tod = 'Morning'
    elif 12 <= hour < 18: tod = 'Afternoon'
    elif 18 <= hour < 22: tod = 'Evening'
    else:                  tod = 'Night'
    tod_col = f'Time_of_Day_{tod}'
    if tod_col in input_data:
        input_data[tod_col] = 1

    # Humidity Category
    if humidity < 40:    hcat = 'Dry'
    elif humidity < 60:  hcat = 'Normal'
    elif humidity < 80:  hcat = 'Humid'
    else:                hcat = 'Very_Humid'
    hcat_col = f'Humidity_Category_{hcat}'
    if hcat_col in input_data:
        input_data[hcat_col] = 1

    # Wind Category
    if wind_spd < 5:     wcat = 'Calm'
    elif wind_spd < 15:  wcat = 'Light'
    elif wind_spd < 30:  wcat = 'Moderate'
    else:                wcat = 'Strong'
    wcat_col = f'Wind_Category_{wcat}'
    if wcat_col in input_data:
        input_data[wcat_col] = 1

    # Build final DataFrame in exact feature order
    X_input = pd.DataFrame([input_data])[FEATURES]

    # ── Predict ──────────────────────────────────────────────────────────────
    pred = model.predict(X_input)[0]
    aqi_24h = max(0, round(pred[0]))
    aqi_48h = max(0, round(pred[1]))

    risk_24h = get_risk_level(aqi_24h)
    risk_48h = get_risk_level(aqi_48h)
    _, _, color_24h, advice_24h = AQI_LEVELS[risk_24h]
    _, _, color_48h, advice_48h = AQI_LEVELS[risk_48h]

    # ── Display results ───────────────────────────────────────────────────────
    st.subheader(f"📊 AQI Forecast for {city}")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Current AQI", current_aqi, delta=None)
        cur_risk = get_risk_level(current_aqi)
        st.markdown(f"<span style='color:{AQI_LEVELS[cur_risk][2]};font-weight:bold'>{cur_risk}</span>",
                    unsafe_allow_html=True)
    with col_b:
        delta_24 = aqi_24h - current_aqi
        st.metric("24-Hour Forecast", aqi_24h,
                  delta=f"{delta_24:+d}", delta_color="inverse")
        st.markdown(f"<span style='color:{color_24h};font-weight:bold'>{risk_24h}</span>",
                    unsafe_allow_html=True)
    with col_c:
        delta_48 = aqi_48h - current_aqi
        st.metric("48-Hour Forecast", aqi_48h,
                  delta=f"{delta_48:+d}", delta_color="inverse")
        st.markdown(f"<span style='color:{color_48h};font-weight:bold'>{risk_48h}</span>",
                    unsafe_allow_html=True)

    st.divider()

    # Health advice
    col_d, col_e = st.columns(2)
    with col_d:
        st.markdown(f"""
        <div style="padding:16px;border-radius:10px;background-color:{color_24h}22;
                    border-left:4px solid {color_24h}">
            <b>24-Hour Advisory</b><br>{advice_24h}
        </div>""", unsafe_allow_html=True)
    with col_e:
        st.markdown(f"""
        <div style="padding:16px;border-radius:10px;background-color:{color_48h}22;
                    border-left:4px solid {color_48h}">
            <b>48-Hour Advisory</b><br>{advice_48h}
        </div>""", unsafe_allow_html=True)

    # Early warning banner
    st.divider()
    if risk_24h in ['Poor', 'Very Poor', 'Severe'] or risk_48h in ['Poor', 'Very Poor', 'Severe']:
        st.error(f"⚠️ **Early Warning** — Elevated pollution levels forecast for {city}. "
                 f"24h: **{risk_24h}** (AQI {aqi_24h}) | 48h: **{risk_48h}** (AQI {aqi_48h})")
    else:
        st.success(f"✅ Air quality forecast looks acceptable for {city} over the next 48 hours.")

else:
    # ── Welcome / instructions ────────────────────────────────────────────────
    st.info("👈 Set the weather and pollutant values in the sidebar, then click **Predict AQI**.")

    st.markdown("""
    ### How to use this app
    1. **Select a city** from the dropdown (29 cities across India)
    2. **Enter current weather conditions** — temperature, humidity, wind speed, etc.
    3. **Enter current pollutant levels** — PM2.5, PM10, NO₂, O₃, CO, SO₂
    4. **Click Predict AQI** to get the 24h and 48h forecast

    ### Cities covered
    """)
    # Show all cities as a nice grid
    city_rows = [CITIES[i:i+5] for i in range(0, len(CITIES), 5)]
    for row in city_rows:
        st.markdown("  •  ".join(row))

    st.markdown("""
    ---
    ### AQI Scale Reference
    | Category | AQI Range | Meaning |
    |---|---|---|
    | 🟢 Good | 0–50 | Air quality is satisfactory |
    | 🟡 Moderate | 51–100 | Acceptable; sensitive groups take care |
    | 🟠 Poor | 101–200 | Unhealthy for sensitive groups |
    | 🔴 Very Poor | 201–300 | Unhealthy for everyone |
    | 🟣 Severe | 301+ | Hazardous — avoid outdoors |
    """)
