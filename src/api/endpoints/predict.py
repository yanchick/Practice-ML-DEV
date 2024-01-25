from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends

from src.api.schemas.auth_schema import User
from src.api.schemas.predict_schema import PredictionResponce
from src.infrastructure.services.predict_service import PredictionService, get_prediction_service
from src.infrastructure.core.security import get_current_user

router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/prediction")
async def send_data_for_prediction(model_name: str,
                                   prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                   file: UploadFile = File(...), user: User = Depends(get_current_user)):
    prediction_id = await prediction_service.register_prediction(user_id=user.id, model=model_name, file=file)
    return prediction_id


@router.get("/prediction_result")
async def get_prediction_results(prediction_id: str,
                                 prediction_service: Annotated[PredictionService, Depends(get_prediction_service)],
                                 user: User = Depends(get_current_user)):
    prediction = await prediction_service.get_predictions(user_id=user.id,
                                                          prediction_id=prediction_id)
    responce = PredictionResponce.get_from_db(prediction)

    return responce
