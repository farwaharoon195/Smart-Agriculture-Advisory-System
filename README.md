# Smart Agriculture Advisory System

A complete, runnable smart farming advisory application built with FastAPI.

## Features

- Web form UI for farmers/agronomists to input field conditions.
- Advisory engine that generates:
  - irrigation recommendation
  - fertilization recommendation
  - pest-control action
  - overall risk level
- JSON API endpoint for integration with mobile or IoT clients.
- Health endpoint for uptime checks.
- Automated tests and GitHub Actions CI workflow.

## Tech Stack

- Python 3.11+
- FastAPI
- Jinja2 templates
- Pytest

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open: http://127.0.0.1:8000

## API Example

`POST /api/v1/advice`

```json
{
  "crop": "maize",
  "temperature_c": 33,
  "humidity_pct": 70,
  "soil_moisture_pct": 25,
  "rainfall_mm": 2,
  "pest_alert": "medium"
}
```

## Run Tests

```bash
pytest -q
```

## Project Structure

```text
.
├── app.py
├── templates/index.html
├── tests/test_app.py
├── requirements.txt
└── .github/workflows/ci.yml
```
