from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.auth import CurrentUser
from src.repository.predictions import PredictionRepository
from src.schemes.model_schemes import AvailableModels
from src.schemes.prediction_schemes import RequestPrediction
from src.schemes.router import OpenAPIResponses, Session
from src.schemes.user_schemes import PredictionItem, PredictionScheme
from rq import Queue
from redis import Redis
from src.settings import Settings
from src.tasks import dummy_prediction

router = APIRouter(prefix="/prediction", tags=["prediction"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)
settings = Settings()
queue = Queue(connection=Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password))


@router.get("/")
async def get_user_predictions(user: CurrentUser, session: Session) -> PredictionScheme:
    predictions = await PredictionRepository.get_predictions_by_user_id(user.id, session)
    return PredictionScheme(predictions=[PredictionItem(result=prediction.predicted_class) for prediction in predictions])


@router.post("/predict")
async def predict(model_name: AvailableModels, data: RequestPrediction, user: CurrentUser, session: Session) -> JSONResponse:
    # todo todo todo change model id
    predictions = await PredictionRepository.create_predictions(user.id, 1, data.data, session)
    match model_name:
        case AvailableModels.dummy:
            res = queue.enqueue(dummy_prediction, data=data.data, prediction_ids=[prediction.id for prediction in predictions])
        case _:
            raise ValueError
    print(res)
    return JSONResponse({"result": "ok"})


@router.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: int, user: CurrentUser, session: Session) -> PredictionScheme:
    prediction = await PredictionRepository.get_prediction_by_id(prediction_id, session)
    return PredictionScheme(predictions=[PredictionItem(result=prediction.predicted_class)])
