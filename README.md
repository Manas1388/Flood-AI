# 🌊 Flood-AI 🤖

**AI-based Flood Risk Prediction System using Real-Time Weather Data**

---

## 📌 Overview

Flood-AI is an intelligent disaster-prediction system that estimates flood risk for selected cities using real-time weather data and a machine learning model. The system analyzes environmental factors such as rainfall, humidity, pressure, temperature, and wind speed to compute a flood risk score and generate alerts.

This project is designed for disaster management support, early warning systems, and research applications.

---

## ✨ Features

* 🌧️ Machine Learning model for flood risk prediction
* 🌍 Real-time weather data using OpenWeatherMap API
* 📊 Automated model training from dataset
* ⚠️ Risk classification (LOW / MEDIUM / HIGH)
* 📧 Email alert system for high-risk situations
* ☁️ Cloud deployment ready (AWS EC2 compatible)
* 🧠 Disaster early warning support system

---

## 🛠️ Technologies Used

* Python 3.x
* Scikit-learn (Machine Learning)
* Pandas & NumPy (Data Processing)
* OpenWeatherMap API (Weather Data)
* SMTP (Email Alerts)
* AWS EC2 (Cloud Deployment)

---

## 📂 Project Structure

```
Flood-AI/
│
├── model.py            # Main application script
├── requirements.txt    # Python dependencies
├── train_sample.csv    # Sample dataset for training
├── .gitignore          # Ignored files
└── README.md           # Project documentation
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Flood-AI.git
cd Flood-AI
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Configure API Key

Open `model.py` and replace with your own OpenWeatherMap API key:

```
API_KEY = "YOUR_API_KEY"
```

You can obtain a free API key from:
👉 https://openweathermap.org/api

---

## ▶️ How to Run

```
python model.py
```

You will be prompted to enter city names:

```
Enter city names (comma separated): Delhi, Mumbai
```

---

## 📊 How It Works

1. Loads training dataset
2. Trains a Random Forest regression model
3. Fetches real-time weather data
4. Predicts flood risk score
5. Classifies risk level
6. Sends alert if risk is high

---

## 🚨 Risk Levels

| Risk Score | Status                    |
| ---------- | ------------------------- |
| Low        | Situation safe            |
| Medium     | Monitor conditions        |
| High       | Immediate action required |

---

## 📧 Email Alert System

When high flood risk is detected, the system automatically sends an alert email to the configured recipient.

Configure in `model.py`:

```
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "app_password"
EMAIL_RECEIVER = "receiver@gmail.com"
```

⚠️ Use an App Password (not your main Gmail password)

---

## ☁️ Cloud Deployment (AWS EC2)

Flood-AI is designed to run on cloud servers for continuous monitoring.

Basic deployment steps:

```
sudo apt update
sudo apt install python3-pip -y
git clone <repo_url>
cd Flood-AI
pip3 install -r requirements.txt
python3 model.py
```

---

## 🎯 Applications

* Disaster management agencies
* Early warning systems
* Smart city monitoring
* Environmental research
* Academic projects

---

## 🔮 Future Enhancements

* SMS alerts integration
* Web dashboard interface
* Mobile application
* IoT sensor integration
* Deep learning models
* Multi-hazard prediction

---

## 👤 Author

**Manas Amoli**
B.Tech AIML — Chandigarh University

---

## ⚠️ Disclaimer

This system provides predictive estimates based on available data and should not replace official disaster warnings.

---

## ⭐ Support

If you find this project useful, consider giving it a star ⭐ on GitHub.
