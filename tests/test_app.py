from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health():
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_api_advice_response_schema():
    payload = {
        "crop": "maize",
        "temperature_c": 33,
        "humidity_pct": 70,
        "soil_moisture_pct": 25,
        "rainfall_mm": 2,
        "pest_alert": "medium",
    }
    resp = client.post('/api/v1/advice', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"irrigation", "fertilization", "pest_control", "risk_level"}
    assert data["risk_level"] in {"low", "medium", "high"}


def test_home_renders():
    resp = client.get('/')
    assert resp.status_code == 200
    assert "Smart Agriculture Advisory System" in resp.text
