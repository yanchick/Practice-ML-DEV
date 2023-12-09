from typing import Annotated

from fastapi import APIRouter, Depends

from src.database import User
from src.router.auth import get_current_user
from src.schemes.user_scemes import PredictionItem, PredictionScheme

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.get("/")
async def get_user_predictions(user: Annotated[User, Depends(get_current_user)]) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])


@router.post("/predict")
async def predict(user: Annotated[User, Depends(get_current_user)], model_id: int) -> PredictionScheme:
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])
