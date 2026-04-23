# Smart Agriculture Advisory System

A production-ready Flask web application tailored for farmers in Punjab, Pakistan. The platform provides practical advisories for crop planning, disease checks, irrigation decisions, and market-price forecasting.

## Project Overview

The Smart Agriculture Advisory System helps users make data-informed farm decisions through a simple dashboard with multilingual support (English/Urdu), weather insights, and recommendation modules.

## Features

- **Authentication**: Register/Login with secure password hashing
- **Farmer Dashboard**: Single-page advisory operations panel
- **Crop Recommendation**: Rule-based suggestions from soil, season, and weather
- **Disease Detection**: Image filename heuristic or symptom rule-based diagnosis
- **Irrigation Advisory**: Weather-parameter based irrigation guidance
- **Market Price Prediction**: Linear regression model for crop price forecasting
- **Urdu Language Toggle**: Session-based dictionary translation
- **Weather Integration**: OpenWeather API support with automatic mock fallback
- **SMS Alert Simulation**: Console/log simulation after disease advisory
- **Logging System**: Persistent logging to `app.log`

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (auto-initialized)
- **ML/AI**: scikit-learn LinearRegression + rule-based models

## Project Structure

```text
Smart-Agriculture-Advisory-System/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   └── uploads/
├── models/
└── utils/
    ├── __init__.py
    ├── advisory.py
    └── model_utils.py
```

## Installation Steps

1. Clone repo and enter directory:
   ```bash
   git clone <repo_url>
   cd Smart-Agriculture-Advisory-System
   ```
2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run Instructions

```bash
python3 app.py
```

The app runs at `http://127.0.0.1:5000`.

## API Endpoints

- `GET /` — Landing page
- `GET|POST /register` — User registration
- `GET|POST /login` — User login
- `GET /logout` — Logout
- `GET /dashboard` — Main advisory dashboard (auth required)
- `POST /crop` — Crop recommendation
- `POST /disease` — Disease detection
- `POST /irrigation` — Irrigation advisory
- `POST /market` — Market price prediction
- `GET /api/weather?city=Lahore` — Weather data
- `POST /set-language` — Toggle `en`/`ur`

## Screenshots

- `docs/screenshots/dashboard.png` (placeholder)
- `docs/screenshots/advisory-results.png` (placeholder)

## Future Improvements

- Real image-based disease model (CNN)
- Personalized farmer profiles and field histories
- Historical market data ingestion for better predictions
- Real SMS gateway integration (Twilio/local provider)
- Punjabi language support and offline-first mobile UI
