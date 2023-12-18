import sys
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File

sys.path.append(str(Path(__file__).resolve().parents[3]))
from api.v1.schemas.predict_schema import PredictionResponce


router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/predict")
async def send_data_for_prediction(file: UploadFile, model_name: str):
    '''
    Prediction request endpoint
    '''
    return PredictionResponce(2.5)

@router.get("/predict")
async def get_prediction_results(model_name: str):
    '''
    Predictions result endpoint
    '''
    return PredictionResponce(1.2)
