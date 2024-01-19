import sys
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parents[3]))
from infrastructure.database.model import Predictions


class PredictionResult(BaseModel):
    datetime: datetime
    output: float


class PredictionResponce(BaseModel):
    prediction_id: int
    output: Optional[List[PredictionResult]]

    @classmethod
    def get_from_db(cls, db_prediction: Predictions):

        data_dict = db_prediction.output

        if data_dict is None:
            results = None
        else:
            results = [PredictionResult(datetime=datetime.fromisoformat(dt), output=ls)
                       for dt, ls, in zip(data_dict["timestamp"].values(), data_dict["lifespan"].values())]

        responce = PredictionResponce(prediction_id = db_prediction.id,
                                      prediction_model_id=db_prediction.model_id,
                                      created_at=db_prediction.prediction_date,
                                      output=results,
                                      error_info=db_prediction.error_info)
    
        return responce
