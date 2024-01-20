from typing import List

from backend.model.predictor import Predictor
from backend.model.prediction import Prediction
from backend.repository.base_repository import BaseRepository


class PredictorRepository(BaseRepository):
    def __init__(self, session_factory):
        super().__init__(session_factory, Prediction)

    def get_all_predictors(self) -> List[Predictor]:
        with self.session_factory() as session:
            return session.query(Predictor).all()

    def get_predictor_by_name(self, name: str) -> Predictor:
        with self.session_factory() as session:
            return session.query(Predictor).filter(Predictor.name == name).first()
