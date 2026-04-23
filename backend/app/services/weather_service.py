import random


class WeatherProvider:
    def get_weather(self, district: str) -> dict:
        return {
            "district": district,
            "temperature_c": round(random.uniform(22, 41), 1),
            "rain_mm": round(random.uniform(0, 60), 1),
            "humidity": random.randint(20, 90),
        }
