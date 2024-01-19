import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from infrastructure.repository.base_repository import SQLAlchemyRepository
from infrastructure.database.model import Predictions

class PredictionsRepository(SQLAlchemyRepository):
    model = Predictions
