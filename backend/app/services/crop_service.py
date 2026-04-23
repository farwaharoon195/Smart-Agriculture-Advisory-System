class CropRecommendationEngine:
    _rules = {
        ("loamy", "summer"): ["Cotton", "Maize"],
        ("clay", "winter"): ["Wheat", "Mustard"],
        ("sandy", "summer"): ["Millet", "Groundnut"],
    }

    def recommend(self, soil_type: str, season: str, weather: dict) -> list[str]:
        base = self._rules.get((soil_type.lower(), season.lower()), ["Wheat"])
        if weather.get("rain_mm", 0) > 30 and "Rice" not in base:
            base.append("Rice")
        return base
