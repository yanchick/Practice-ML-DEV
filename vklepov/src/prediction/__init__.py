"""Prediction module."""

from .main import predict
from .models import models as prediction_models

__all__ = ["predict", "prediction_models"]
