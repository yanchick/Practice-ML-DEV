from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from src.infrastructure.database.model import Predictions


class PredictionResult(BaseModel):
    datetime: datetime
    output: float


class PredictionResponce(BaseModel):
    prediction_id: int
    output: float
    prediction_model_id: int
    prediction_date: datetime
    error_info: Optional[str]
    is_finished: bool

    @classmethod
    def get_from_db(cls, db_prediction: Predictions):
        responce = PredictionResponce(
            prediction_id=db_prediction.id,
            prediction_model_id=db_prediction.model_id,
            prediction_date=db_prediction.prediction_date,
            output=db_prediction.output,
            error_info=db_prediction.error_info,
            is_finished=db_prediction.is_finished
        )
        return responce
