import sys
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends

sys.path.append(str(Path(__file__).resolve().parents[3]))
from api.v1.schemas.auth_schema import User
from api.v1.schemas.predict_schema import PredictionResponce
from infrastructure.services.predict_service import PredictionService, get_prediction_service
from infrastructure.core.security import get_current_user


router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/{model_name}")
async def send_data_for_prediction(model_name: str, prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                   file: UploadFile = File(...), user: User = Depends(get_current_user)):
    '''
    Prediction request endpoint
    '''

    prediction_id = await prediction_service.register_prediction(user_id=user.id, model=model_name, file=file)
    return prediction_id

@router.get("/{prediction_id}")
async def get_prediction_results(prediction_id: str, prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                 user: User = Depends(get_current_user)):
    '''
    Predictions result endpoint
    '''

    prediction = await prediction_service.get_predictions(user_id=user.id, 
                                                          prediction_id=prediction_id)


    responce = PredictionResponce.get_from_db(prediction)
    
    return responce
