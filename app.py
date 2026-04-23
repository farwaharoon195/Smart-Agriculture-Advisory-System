from __future__ import annotations

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(title="Smart Agriculture Advisory System", version="1.0.0")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class AdvisoryInput(BaseModel):
    crop: str = Field(min_length=2, max_length=30)
    temperature_c: float = Field(ge=-10, le=60)
    humidity_pct: int = Field(ge=0, le=100)
    soil_moisture_pct: int = Field(ge=0, le=100)
    rainfall_mm: float = Field(ge=0, le=400)
    pest_alert: Literal["none", "low", "medium", "high"] = "none"


class AdvisoryResult(BaseModel):
    irrigation: str
    fertilization: str
    pest_control: str
    risk_level: Literal["low", "medium", "high"]


def generate_advisory(data: AdvisoryInput) -> AdvisoryResult:
    if data.soil_moisture_pct < 30 or data.rainfall_mm < 5:
        irrigation = "Irrigate immediately with drip irrigation for 30-45 minutes."
    elif data.soil_moisture_pct < 50:
        irrigation = "Provide moderate irrigation today and monitor tomorrow morning."
    else:
        irrigation = "No immediate irrigation required. Recheck moisture in 24 hours."

    if data.temperature_c > 35:
        fertilization = "Avoid heavy fertilization in peak heat; apply foliar micronutrients in the evening."
    elif data.crop.lower() in {"rice", "maize", "wheat"} and data.soil_moisture_pct >= 40:
        fertilization = "Apply balanced NPK at recommended stage dose with light irrigation after application."
    else:
        fertilization = "Use compost + low-dose nitrogen and reassess after 7 days."

    if data.pest_alert == "high":
        pest_control = "High pest pressure: inspect field borders and apply targeted integrated pest management today."
        risk = "high"
    elif data.pest_alert in {"medium", "low"}:
        pest_control = "Monitor pest traps daily and use bio-control where threshold is crossed."
        risk = "medium"
    else:
        pest_control = "No active pest alert. Keep weekly scouting schedule."
        risk = "low"

    if data.humidity_pct > 85 and data.temperature_c > 28 and risk != "high":
        risk = "medium"

    return AdvisoryResult(
        irrigation=irrigation,
        fertilization=fertilization,
        pest_control=pest_control,
        risk_level=risk,
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": None, "payload": None}
    )


@app.post("/advice", response_class=HTMLResponse)
def advice_form(
    request: Request,
    crop: str = Form(...),
    temperature_c: float = Form(...),
    humidity_pct: int = Form(...),
    soil_moisture_pct: int = Form(...),
    rainfall_mm: float = Form(...),
    pest_alert: str = Form("none"),
):
    payload = AdvisoryInput(
        crop=crop,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        soil_moisture_pct=soil_moisture_pct,
        rainfall_mm=rainfall_mm,
        pest_alert=pest_alert,
    )
    result = generate_advisory(payload)
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": result, "payload": payload}
    )


@app.post("/api/v1/advice", response_model=AdvisoryResult)
def advice_api(payload: AdvisoryInput):
    return generate_advisory(payload)


@app.get("/health")
def health():
    return {"status": "ok"}
