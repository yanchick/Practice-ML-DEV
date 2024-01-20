from typing import List

from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload

from backend.model.prediction_batch import PredictionBatch
from backend.model.predictor import Predictor
from backend.model.prediction import Prediction
from backend.repository.base_repository import BaseRepository


class PredictionRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Prediction)

    def create_prediction(self, prediction_data):
        with self.session_factory() as session:
            prediction = Prediction(**prediction_data)
            session.add(prediction)
            session.commit()
            session.refresh(prediction)
            return prediction

    def create_batch(self, user_id: int, predictor_name: str, transaction_id: int):
        with self.session_factory() as session:
            batch = PredictionBatch(user_id=user_id, predictor_name=predictor_name, transaction_id=transaction_id)
            session.add(batch)
            session.commit()
            session.refresh(batch)
            return batch

    def get_predictions_reports(self):
        with self.session_factory() as session:
            prediction_reports = session.query(Predictor.name, func.count(Prediction.id).label('total_predictions')) \
                .join(PredictionBatch, Prediction.batch_id == PredictionBatch.id) \
                .join(Predictor, PredictionBatch.predictor_name == Predictor.name) \
                .group_by(Predictor.name).all()

            return prediction_reports

    def get_prediction_history(self, user_id: int) -> List[PredictionBatch]:
        with self.session_factory() as session:
            prediction_batches = session.query(PredictionBatch) \
                .options(joinedload(PredictionBatch.predictions),
                         joinedload(PredictionBatch.transaction),
                         joinedload(PredictionBatch.predictor)) \
                .filter(PredictionBatch.user_id == user_id) \
                .order_by(desc(PredictionBatch.created_at)) \
                .all()
            return prediction_batches
