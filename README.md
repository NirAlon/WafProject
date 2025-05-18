# 🛡️ WAF Demo Dashboard

A lightweight Web Application Firewall (WAF) demo that uses machine learning models to detect XSS and SQL Injection attacks. The system includes a Flask frontend, an orchestration API, and trained time series (TS) models. Deployed using Docker Compose for modularity and scalability.


## 🚀 Features

- ✅ Flask-based web UI for testing payloads
- ✅ Real-time ML-powered detection of XSS & SQLi
- ✅ SQLite database with log persistence
- ✅ Displays client IP & location via IP geolocation API
- ✅ Live update of results using Socket.IO
- ✅ Docker Compose orchestration for local development

---

## 🐳 Getting Started (with Docker Compose)

### 1. Clone the repo

```bash
git clone https://github.com/NirAlon/waf-demo.git
cd waf-demo
```

### 2. Build and run

```bash
docker-compose up --build
```

#### Frontend will be available at: 👉 http://localhost:8003

## 🧠 How It Works

1. Users input a test payload and attack type (XSS or SQLi) via the web UI.

2. The Flask app sends the payload to the orchestration API.

3. The orchestrator routes the request to the appropriate ML model.

4. The model returns a score indicating whether the payload is malicious.

5. The result is logged (along with IP/location) and shown in real-time on the dashboard.

## 🧪 Example Payloads
* SQLi:
```OR 1=1 --```

* XSS: ```<script>alert("XSS ATTACK")</script>```


## built With

* Python (Flask, SQLAlchemy, requests)
* TensorFlow / Scikit-learn (ML models)
* Chart.js & Bootstrap (Frontend UI)
* Docker & Docker Compose
* Socket.IO (Live updates)
* ipapi.co (for IP geolocation)

## 📜 License
MIT License © 2025 Nir Alon


## 👤 Author
Nir Alon | Backend Engineer | ML Security Enthusiast | Infra Builder