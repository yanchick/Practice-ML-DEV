from src.infrastructure.repository.base_repository import SQLAlchemyRepository
from src.infrastructure.database.model import Predictions


class PredictionsRepository(SQLAlchemyRepository):
    model = Predictions
