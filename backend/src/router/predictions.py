from fastapi import APIRouter

from src.auth import CurrentUser
from src.schemes.router import OpenAPIResponses
from src.schemes.user_schemes import PredictionItem, PredictionScheme

router = APIRouter(prefix="/prediction", tags=["prediction"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)


@router.get("/")
async def get_user_predictions(user: CurrentUser) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])


@router.post("/predict")
async def predict(model_id: int, user: CurrentUser) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])


@router.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: int, user: CurrentUser) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])
