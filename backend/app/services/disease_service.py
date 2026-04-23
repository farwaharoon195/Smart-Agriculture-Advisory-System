class DiseaseDetector:
    _symptom_map = {
        "yellow_spots": "Leaf Rust",
        "white_powder": "Powdery Mildew",
        "wilting": "Bacterial Wilt",
    }

    def predict(self, symptoms: list[str]) -> dict:
        for symptom in symptoms:
            if symptom in self._symptom_map:
                return {"disease": self._symptom_map[symptom], "confidence": 0.82}
        return {"disease": "Healthy/Unknown", "confidence": 0.55}
