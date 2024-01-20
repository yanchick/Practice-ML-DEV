from pathlib import Path
from typing import Dict, List

import joblib

from backend.repository.predictor_repository import PredictorRepository


def load_model(model_name):
    model_names = {
        'DecisionTree': 'DecisionTreeClassifier_best_model.pkl',
        'RandomForest': 'RandomForestClassifier_best_model.pkl',
        'GradientBoosting': 'GradientBoostingClassifier_best_model.pkl',
    }
    model_file = model_names[model_name]
    current_file_path = Path(__file__).resolve()
    project_root = current_file_path.parents[2]
    models_directory = project_root / 'ml/models'
    full_model_path = models_directory / model_file

    if not full_model_path.exists():
        raise FileNotFoundError(f"Model file not found at {full_model_path}")
    return joblib.load(full_model_path)


class PredictorService:
    def __init__(self, predictor_repository: PredictorRepository):
        self.predictor_repository = predictor_repository

    def get_available_models(self) -> List[Dict[str, str]]:
        available_models = []
        predictors = self.predictor_repository.get_all_predictors()
        for predictor in predictors:
            available_models.append({
                "name": predictor.name,
                "cost": predictor.cost
            })
        return available_models

    def get_model_cost(self, model_name: str) -> int:
        predictor = self.predictor_repository.get_predictor_by_name(model_name)
        if predictor:
            return predictor.cost
        raise ValueError(f"Model {model_name} is not available.")
