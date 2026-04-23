import logging

logger = logging.getLogger(__name__)


def recommend_crops(soil, season, weather):
    soil = soil.lower()
    season = season.lower()
    weather = weather.lower()

    rules = {
        ("loamy", "rabi"): ["Wheat", "Mustard"],
        ("clay", "kharif"): ["Rice", "Sugarcane"],
        ("sandy", "kharif"): ["Cotton", "Millet"],
    }

    base = rules.get((soil, season), ["Maize", "Vegetables"])
    if "hot" in weather:
        base.append("Sunflower")
    if "rain" in weather:
        base.append("Pulses")
    return sorted(set(base))


def detect_disease_by_image_name(filename):
    lower = filename.lower()
    if "rust" in lower:
        return "Likely Leaf Rust detected"
    if "blight" in lower:
        return "Likely Blight detected"
    if "spot" in lower:
        return "Likely Leaf Spot detected"
    return "No obvious disease detected (rule-based scan)"


def irrigation_advice(temperature, humidity, rainfall):
    if rainfall > 20:
        return "Skip irrigation for next 24 hours due to adequate rainfall."
    if temperature > 35 and humidity < 40:
        return "High evapotranspiration risk: irrigate early morning and evening."
    if temperature < 20 and humidity > 60:
        return "Reduce irrigation; monitor soil moisture to prevent root rot."
    return "Moderate conditions: irrigate once today and re-evaluate tomorrow."


def simulate_sms_alert(farmer_name, message):
    logger.info("SMS ALERT to %s: %s", farmer_name, message)
