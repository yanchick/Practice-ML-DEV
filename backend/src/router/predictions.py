from fastapi import APIRouter

from src.auth import CurrentUser
from src.schemes.user_scemes import PredictionItem, PredictionScheme

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.get("/")
async def get_user_predictions(user: CurrentUser) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])


@router.post("/predict")
async def predict(user: CurrentUser, model_id: int) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])
