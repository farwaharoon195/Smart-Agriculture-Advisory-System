from flask import Blueprint, request, jsonify
from app.core.db import SessionLocal
from app.repositories.user_repo import UserRepository
from app.services.crop_service import CropRecommendationEngine
from app.services.disease_service import DiseaseDetector
from app.services.irrigation_service import IrrigationAdvisor
from app.services.market_service import MarketPricePredictor
from app.services.weather_service import WeatherProvider
from app.services.sms_service import SmsAlertService

api_bp = Blueprint("api", __name__)

crop_engine = CropRecommendationEngine()
disease_detector = DiseaseDetector()
irrigation_advisor = IrrigationAdvisor()
market_predictor = MarketPricePredictor()
weather_provider = WeatherProvider()
sms_service = SmsAlertService()


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "smart-agri-api"})


@api_bp.post("/users/register")
def register_user():
    payload = request.get_json()
    session = SessionLocal()
    try:
        repo = UserRepository(session)
        user = repo.create(payload)
        return jsonify({"id": user.id, "name": user.name, "phone": user.phone}), 201
    finally:
        session.close()


@api_bp.post("/recommend/crop")
def recommend_crop():
    payload = request.get_json()
    weather = payload.get("weather") or weather_provider.get_weather(payload["district"])
    crops = crop_engine.recommend(payload["soil_type"], payload["season"], weather)
    return jsonify({"recommended_crops": crops, "weather": weather})


@api_bp.post("/detect/disease")
def detect_disease():
    payload = request.get_json()
    result = disease_detector.predict(payload.get("symptoms", []))
    return jsonify(result)


@api_bp.post("/advisory/irrigation")
def irrigation_advice():
    payload = request.get_json()
    result = irrigation_advisor.schedule(payload["temperature_c"], payload["rain_mm"])
    return jsonify(result)


@api_bp.get("/predict/market-price")
def predict_market_price():
    month = int(request.args.get("month", "1"))
    price = market_predictor.predict(month)
    return jsonify({"month": month, "predicted_price_pkr_per_40kg": round(price, 2)})


@api_bp.post("/alerts/sms")
def send_sms_alert():
    payload = request.get_json()
    status = sms_service.send(payload["phone"], payload["message"])
    return jsonify(status)
