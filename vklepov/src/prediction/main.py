"""Prediction module."""

import pandas as pd
from io import BytesIO
import joblib


def predict(model_name: str, data_file: BytesIO):
    model = joblib.load(f"./models/{model_name}.joblib")
    data = pd.read_csv(data_file)
    X = data[model.feature_names_in_].dropna()
    return model.predict(X)
