from sqlalchemy import update

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.predictions import Prediction


class PredictionRepository:
    @staticmethod
    async def get_predictions_by_user_id(user_id: int, session: AsyncSession) -> list[Prediction] | None:
        query = select(Prediction).where(Prediction.user_id == user_id)
        result = (await session.scalars(query)).all()
        return result

    @staticmethod
    async def create_predictions(
        user_id: int, model_id: int, data: list[str], session: AsyncSession
    ) -> list[Prediction]:
        predictions = [
            Prediction(user_id=user_id, model_id=model_id, input_data=prediction_data) for prediction_data in data
        ]
        session.add_all(predictions)
        await session.commit()
        return predictions

    @staticmethod
    async def update_prediction(prediction_ids: list[int], predicted_classes: list[int], session: AsyncSession) -> None:
        for prediction_id, predicted_class in zip(prediction_ids, predicted_classes):
            query = update(Prediction).where(Prediction.id == prediction_id).values(predicted_class_id=predicted_class)
            await session.execute(query)
        await session.commit()

    @staticmethod
    async def get_prediction_by_id(prediction_id: int, session: AsyncSession) -> Prediction:
        prediction = await session.get_one(Prediction, prediction_id)
        return prediction
