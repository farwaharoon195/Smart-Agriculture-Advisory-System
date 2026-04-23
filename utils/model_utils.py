import os
import pickle

import numpy as np
from sklearn.linear_model import LinearRegression

CROP_MAP = {
    "wheat": 0,
    "rice": 1,
    "cotton": 2,
    "sugarcane": 3,
}


def _training_data():
    # Features: crop_id, month, rainfall_mm, fuel_cost
    x = np.array(
        [
            [0, 1, 20, 250],
            [0, 2, 15, 255],
            [0, 3, 12, 265],
            [1, 7, 180, 250],
            [1, 8, 210, 260],
            [2, 9, 50, 255],
            [2, 10, 30, 265],
            [3, 11, 15, 270],
            [3, 12, 10, 275],
        ]
    )
    # Target: approximate PKR per 40kg
    y = np.array([3100, 3200, 3300, 4800, 5000, 7500, 7800, 4200, 4400])
    return x, y


def load_or_train_price_model(model_path):
    if os.path.exists(model_path):
        with open(model_path, "rb") as model_file:
            return pickle.load(model_file)

    x, y = _training_data()
    model = LinearRegression()
    model.fit(x, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)

    return model


def predict_market_price(model, crop, month, rainfall, fuel_cost):
    crop_id = CROP_MAP.get(crop.lower(), 0)
    features = np.array([[crop_id, month, rainfall, fuel_cost]])
    return float(model.predict(features)[0])
