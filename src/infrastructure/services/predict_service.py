from pathlib import Path

import pandas as pd
from rq.decorators import job


from src.infrastructure.core.exceptions import NotFoundError, DuplicatedError
from src.infrastructure.repository.base_repository import AbstractRepository
from src.infrastructure.repository.user_repository import UserRepository
from src.infrastructure.repository.predictions_repository import PredictionsRepository
from src.infrastructure.repository.models_repository import ModelsRepository
from src.inference.task import predict


TEMP_DIR = Path("data")


class PredictionService:
    def __init__(self, prediction_repo: AbstractRepository, models_repo: AbstractRepository,
                 user_repo: AbstractRepository):
        self.prediction_repo: AbstractRepository = prediction_repo()
        self.models_repo: AbstractRepository = models_repo()
        self.user_repo: AbstractRepository = user_repo()
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    @job("default", timeout=-1)
    def enqueue_predict_task(self, *args, **kwargs):
        return predict(*args, **kwargs)

    async def register_prediction(self, user_id: int, model: str, **kwargs):
        db_model = await self.models_repo.find_by_options(name=model, unique=True)
        db_user = await self.user_repo.find_by_options(id=user_id, unique=True)

        if db_model is None:
            raise NotFoundError(detail="Model not found")

        if db_user.balance < db_model.cost:
            raise DuplicatedError(detail="Not enough credits")

        await self.user_repo.update({"balance": db_user.balance - db_model.cost}, id=user_id)

        prediction_data = {"model_id": db_model.id, "user_id": user_id}
        prediction_id = await self.prediction_repo.add(data=prediction_data)

        if "file" in kwargs:
            data_filename = str(prediction_id) + ".csv"

            df = pd.read_csv(kwargs["file"].file)
            df.to_csv(TEMP_DIR / data_filename, index=False)

            kwargs["file"] = str(TEMP_DIR / data_filename)

        await self.enqueue_predict_task(prediction_id, db_model.name, db_model.cost, db_user.id, db_user.balance, **kwargs)

        return prediction_id

    async def get_predictions(self, user_id: int, prediction_id: int = None):
        if prediction_id is None:
            predictions = await self.prediction_repo.find_by_options(user_id=user_id)
        else:
            predictions = await self.prediction_repo.find_by_options(id=prediction_id,
                                                                     user_id=user_id,
                                                                     unique=True)
        return predictions


def get_prediction_service():
    return PredictionService(prediction_repo=PredictionsRepository, models_repo=ModelsRepository,
                             user_repo=UserRepository)