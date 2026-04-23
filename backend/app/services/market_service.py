import numpy as np
from sklearn.linear_model import LinearRegression


class MarketPricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        x = np.array([[1], [2], [3], [4], [5]])
        y = np.array([2800, 2950, 3100, 3200, 3350])
        self.model.fit(x, y)

    def predict(self, month: int) -> float:
        return float(self.model.predict(np.array([[month]]))[0])
