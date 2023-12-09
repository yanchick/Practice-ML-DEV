from typing import List

from fastapi import APIRouter, UploadFile, File

from service.api.schemas import PredictionResponce


router = APIRouter(prefix="/predictions", tags=["predictions"])



@router.post("from-file/{model}")
async def create_prediction(model: str, file: UploadFile = File()) -> List[PredictionResponce]:
    """Make predictions if hours in file is normal or anomaly"""
    # TODO: add validation for columns and datetimes

    return [PredictionResponce(is_anomaly=True, anomaly_probability=0.5)]

@router.get("by-date/{model}")
async def create_prediction(model: str, start_datetime: str, end_datetime: str) -> List[PredictionResponce]:
    """Make predictions if hours in period form start_datetime to end_datetime is normal or anomaly"""

    return [PredictionResponce(is_anomaly=True, anomaly_probability=0.5)]
