import bentoml
import numpy as np
import pandas as pd

#Ce service est une version 'oldschool' de service.py qui permet de faire des prévisions sur un ensemble de batiments
#On lui passe donc un dataFrame en paramètre, ce qui n'est pas recommandé normalement.

@bentoml.service()
class EnergyPrediction:
    energy_predictor = bentoml.models.get("grid_xgb_regressor:latest")
    scaler = energy_predictor.custom_objects["scaler"]
    feature_names = energy_predictor.custom_objects["feature_names"]

    def __init__(self):
        self.regressor = bentoml.xgboost.load_model(self.energy_predictor)

    @bentoml.api
    #On transforme le dateframe en une liste de chiffre (car une prediction est un nombre)
    def predict(self, data:pd.DataFrame) -> np.ndarray:
        predicted_consumptions = self.regressor.predict(data)
        return (predicted_consumptions)