class IrrigationAdvisor:
    def schedule(self, temperature_c: float, rain_mm: float) -> dict:
        if rain_mm > 20:
            return {"advice": "Skip irrigation for 2 days", "frequency_days": 2}
        if temperature_c > 35:
            return {"advice": "Irrigate daily (light)", "frequency_days": 1}
        return {"advice": "Irrigate every 3 days", "frequency_days": 3}
