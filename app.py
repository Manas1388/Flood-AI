import streamlit as st
import pandas as pd
import joblib
import requests
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# =========================
# API KEY
# =========================
API_KEY = "71c8e280f458588017f4c5dc6b97a53f"

# =========================
# LOAD MODEL
# =========================
model = joblib.load("flood_model.pkl")

data_template = pd.read_csv("train_sample.csv").drop(columns=["FloodProbability"])

# =========================
# GEOPY MAP
# =========================
geolocator = Nominatim(user_agent="flood_ai")

# =========================
# PAGE TITLE
# =========================
st.title("🌊 AI Flood Risk Prediction Dashboard")

cities_input = st.text_input("Enter City Names (comma separated)")

if st.button("Predict Flood Risk"):

    cities = [c.strip() for c in cities_input.split(",")]

    risk_results = []
    map_data = []

    for city in cities:

        st.markdown("---")
        st.header(f"📍 {city}")

        # =========================
        # CURRENT WEATHER
        # =========================
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=71c8e280f458588017f4c5dc6b97a53f&units=metric"

        weather = requests.get(weather_url).json()

        if weather.get("cod") != 200:
            st.error(f"City not found: {city}")
            continue

        temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind = weather["wind"]["speed"]

        rain_1h = weather.get("rain", {}).get("1h", 0)

        # =========================
        # 24H FORECAST RAIN
        # =========================
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=71c8e280f458588017f4c5dc6b97a53f&units=metric"

        forecast = requests.get(forecast_url).json()

        rain_24h = 0

        for item in forecast.get("list", [])[:8]:
            rain_24h += item.get("rain", {}).get("3h", 0)

        # =========================
        # DISPLAY WEATHER
        # =========================
        st.subheader("🌤 Current Weather Data")

        st.write("Temperature:", temp, "°C")
        st.write("Humidity:", humidity, "%")
        st.write("Pressure:", pressure, "hPa")
        st.write("Wind Speed:", wind, "m/s")
        st.write("Rain (1 hour):", rain_1h, "mm")
        st.write("Rain (24 hours):", round(rain_24h,2), "mm")

        # =========================
        # WEATHER GRAPH
        # =========================
        st.subheader("📊 Weather Factors")

        features = ["Temp","Humidity","Pressure","Wind","Rain24h"]
        values = [temp, humidity, pressure/10, wind*10, rain_24h*10]

        fig, ax = plt.subplots()
        ax.bar(features, values)
        ax.set_title("Weather Conditions")
        st.pyplot(fig)

        # =========================
        # MODEL INPUT
        # =========================
        input_row = data_template.iloc[0:1].copy()
        input_row[:] = 0

        for col in input_row.columns:

            c = col.lower()

            if "temp" in c:
                input_row[col] = temp

            elif "humid" in c:
                input_row[col] = humidity

            elif "press" in c:
                input_row[col] = pressure

            elif "wind" in c:
                input_row[col] = wind

            elif "rain" in c:
                input_row[col] = rain_24h

        # =========================
        # PREDICT FLOOD RISK
        # =========================
        risk = model.predict(input_row)[0]
        risk_percent = round(risk*100,2)

        risk_results.append((city,risk_percent))

        st.subheader("🌊 Flood Risk Prediction")
        st.write("Risk Score:", risk_percent,"%")

        if risk > 0.8:
            st.error("🔴 HIGH FLOOD RISK")

        elif risk > 0.4:
            st.warning("🟠 MODERATE FLOOD RISK")

        else:
            st.success("🟢 LOW FLOOD RISK")

        # =========================
        # MAP DATA
        # =========================
        location = geolocator.geocode(city)

        if location:
            map_data.append({
                "city":city,
                "lat":location.latitude,
                "lon":location.longitude,
                "risk":risk_percent
            })

    # =========================
    # CITY COMPARISON GRAPH
    # =========================
    if len(risk_results) > 1:

        st.markdown("---")
        st.header("📊 Flood Risk Comparison")

        cities_names = [c[0] for c in risk_results]
        risks = [c[1] for c in risk_results]

        fig2, ax2 = plt.subplots()

        ax2.bar(cities_names, risks)

        ax2.set_ylabel("Flood Risk %")
        ax2.set_title("City Flood Risk Comparison")

        st.pyplot(fig2)

    # =========================
    # FEATURE IMPORTANCE GRAPH
    # =========================
    st.markdown("---")
    st.header("🧠 AI Model Feature Importance")

    try:

        importances = model.feature_importances_
        feature_names = data_template.columns

        imp_df = pd.DataFrame({
            "Feature":feature_names,
            "Importance":importances
        })

        imp_df = imp_df.sort_values(by="Importance",ascending=False)

        fig3, ax3 = plt.subplots()

        ax3.barh(imp_df["Feature"], imp_df["Importance"])
        ax3.invert_yaxis()

        ax3.set_title("Factors Affecting Flood Prediction")

        st.pyplot(fig3)

    except:
        st.write("Feature importance not available for this model.")

    # =========================
    # FLOOD RISK MAP
    # =========================
    st.markdown("---")
    st.header("🌍 Flood Risk Map")

    if len(map_data) > 0:

        map_df = pd.DataFrame(map_data)

        st.map(map_df.rename(columns={"lat":"latitude","lon":"longitude"}))