from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from backend.utils.date import get_now


class PredictionFeatures(BaseModel):
    merchant_id: int = Field(..., description="Merchant ID for the prediction.")
    cluster_id: int = Field(..., description="Cluster ID for the prediction.")


class PredictionTarget(BaseModel):
    category_id: int = Field(..., description="Predicted Category ID.")
    category_label: Optional[str] = Field(None, description="Label of the predicted Category.")


class PredictionInfo(BaseModel):
    features: PredictionFeatures
    target: PredictionTarget


class PredictionRequest(BaseModel):
    model_name: str = Field(..., example="RandomForest", description="Name of the prediction model to use.")
    features: List[PredictionFeatures] = Field(..., description="List of predictions to make.")


class PredictionBatchInfo(BaseModel):
    id: int
    model_name: str
    predictions: List[PredictionInfo]
    timestamp: datetime = Field(default_factory=get_now(), description="Timestamp of the prediction batch.")
    cost: int = Field(..., description="Total cost of this batch of predictions.")


class PredictionsReport(BaseModel):
    model_name: str = Field(..., description="Name of the prediction model.")
    total_prediction_batches: int = Field(..., description="Total number of prediction batches made using this model.")
