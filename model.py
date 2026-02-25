import pandas as pd
import numpy as np
import requests
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


# ================================
# CONFIGURATION
# ================================

API_KEY = "71c8e280f458588017f4c5dc6b97a53f"   # 🔑 Replace
DATASET_FILE = "train.csv"


# ================================
# TIME STAMP
# ================================

print("\nTime:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# ================================
# LOAD DATASET
# ================================

print("📂 Loading dataset...")
data = pd.read_csv(DATASET_FILE)

print("🧹 Preparing training data...")

X = data.drop("FloodProbability", axis=1)
y = data["FloodProbability"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ================================
# TRAIN MODEL
# ================================

print("🤖 Training AI model...")

model = RandomForestRegressor(
    n_estimators=100,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

print("🔥 Model trained successfully!")


# ================================
# MODEL EVALUATION
# ================================

pred_test = model.predict(X_test)

print("\n📊 Model Performance:")
print("R² Score:", round(r2_score(y_test, pred_test), 4))
print("MAE:", round(mean_absolute_error(y_test, pred_test), 4))


# ================================
# SAVE MODEL
# ================================

joblib.dump(model, "flood_model.pkl")
print("💾 Model saved as flood_model.pkl")


# ================================
# MULTI-CITY INPUT
# ================================

cities_input = input("\n🌍 Enter city names (comma separated): ")
cities = [c.strip() for c in cities_input.split(",")]


# ================================
# PROCESS EACH CITY
# ================================

for city in cities:

    print("\n====================================")
    print("📍 Processing:", city)
    print("====================================")

    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid=71c8e280f458588017f4c5dc6b97a53f&units=metric"
    )

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid=71c8e280f458588017f4c5dc6b97a53f&units=metric"
    )

    weather_res = requests.get(weather_url).json()
    forecast_res = requests.get(forecast_url).json()

    if weather_res.get("cod") != 200:
        print("❌ Failed to fetch weather for", city)
        continue


    # ================================
    # EXTRACT WEATHER DATA
    # ================================

    city_name = weather_res["name"]
    country = weather_res["sys"]["country"]

    temperature = weather_res["main"]["temp"]
    humidity = weather_res["main"]["humidity"]
    pressure = weather_res["main"]["pressure"]
    wind_speed = weather_res["wind"]["speed"]

    rain_1h = weather_res.get("rain", {}).get("1h", 0)


    # ================================
    # CALCULATE 24-HOUR RAIN
    # ================================

    rain_24h = 0
    for item in forecast_res.get("list", [])[:8]:  # 8 x 3h = 24h
        rain_24h += item.get("rain", {}).get("3h", 0)


    # ================================
    # DISPLAY WEATHER
    # ================================

    print("\n📍 Location:", city_name + ",", country)

    print("\n🌤 Weather Conditions:")
    print("Temperature:", temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Pressure:", pressure, "hPa")
    print("Wind Speed:", wind_speed, "m/s")
    print("Rain (1 hour):", rain_1h, "mm")
    print("Rain (24 hours):", rain_24h, "mm")


    # ================================
    # PREPARE INPUT FOR MODEL
    # ================================

    input_values = []

    for col in X.columns:

        c = col.lower()

        if "temp" in c:
            input_values.append(temperature)

        elif "humid" in c:
            input_values.append(humidity)

        elif "press" in c:
            input_values.append(pressure)

        elif "wind" in c:
            input_values.append(wind_speed)

        elif "rain" in c:
            input_values.append(rain_24h)

        else:
            input_values.append(0)


    input_df = pd.DataFrame([input_values], columns=X.columns)


    # ================================
    # PREDICT FLOOD RISK
    # ================================

    risk = model.predict(input_df)[0]

    print("\n🧠 Predicted Flood Risk:",
          round(risk, 3),
          f"({round(risk*100,1)}%)")


    # ================================
    # ALERT SYSTEM
    # ================================

    print("\n🚨 Alert Status:")

    if risk > 0.7:
        print("🔴 HIGH RISK — Immediate action required!")

    elif risk > 0.4:
        print("🟠 MODERATE RISK — Stay alert.")

    else:
        print("🟢 LOW RISK — Situation is safe.")


print("\n✅ System execution completed!")