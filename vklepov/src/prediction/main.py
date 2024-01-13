"""Prediction module."""

import pandas as pd
from io import BytesIO
import joblib


async def predict(model_name: str, data_file: BytesIO, on_finish):
    try:
        model = joblib.load(f"./models/{model_name}.joblib")
        data = pd.read_csv(data_file)
        X = data[model.feature_names_in_].dropna()
        res = model.predict(X)
        await on_finish(True, list(res))
    except Exception as e:
        await on_finish(False, str(e))
