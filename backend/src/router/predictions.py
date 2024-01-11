import pandas as pd
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from rq import Queue

from src.auth import CurrentUser
from src.repository.model import ModelRepository
from src.repository.predictions import PredictionRepository
from src.repository.user import UserRepository
from src.schemes.model_schemes import AvailableModels
from src.schemes.prediction_schemes import RequestPrediction
from src.schemes.router import OpenAPIResponses, Session
from src.schemes.user_schemes import PredictionItem, PredictionScheme
from src.settings import Settings

router = APIRouter(prefix="/prediction", tags=["prediction"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)
settings = Settings()
queue = Queue(connection=Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password))


@router.get("/")
async def get_user_predictions(user: CurrentUser, session: Session) -> PredictionScheme:
    predictions = await PredictionRepository.get_predictions_by_user_id(user.id, session)
    if predictions is None:
        return PredictionScheme(predictions=[])
    return PredictionScheme(
        predictions=[
            PredictionItem(
                id=prediction.id,
                predicted_model_id=prediction.model_id,
                input_data=prediction.input_data,
                result=prediction.predicted_class_id,
            )
            for prediction in predictions
        ]
    )


@router.post("/predict")
async def predict(
    model_name: AvailableModels, data: RequestPrediction, user: CurrentUser, session: Session
) -> JSONResponse:
    model = await ModelRepository.get_model_by_name(model_name, session)
    if model is None:
        raise HTTPException(status_code=400, detail="Model not found")
    await UserRepository.subtract_money(user.id, model.cost, session)
    predictions = await PredictionRepository.create_predictions(user.id, model.id, data.data, session)
    predictions_ids = [prediction.id for prediction in predictions]
    df = pd.DataFrame(data.data, columns=[" Cluster Label"])
    match model_name:
        case AvailableModels.base:
            queue.enqueue("src.tasks.base_model_predict", df, predictions_ids)
        case AvailableModels.logreg_tfidf:
            queue.enqueue("src.tasks.logreg_model_predict", df, predictions_ids)
        case AvailableModels.catboost:
            queue.enqueue("src.tasks.catboost_model_predict", df, predictions_ids)
    return JSONResponse({"result": "ok"})


@router.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: int, user: CurrentUser, session: Session) -> PredictionScheme:
    prediction = await PredictionRepository.get_prediction_by_id(prediction_id, session)
    return PredictionScheme(
        predictions=[
            PredictionItem(
                id=prediction.id,
                predicted_model_id=prediction.model_id,
                input_data=prediction.input_data,
                result=prediction.predicted_class_id,
            )
        ]
    )
