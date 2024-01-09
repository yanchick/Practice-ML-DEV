from typing import List
from model.base_model import Model
from repository.user_repository import UserRepository
from services.base_service import BaseService

class ModelService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_available_models(self) -> List[Model]:
        # Implement the logic to get available models directly using BaseRepository
        # You can modify BaseRepository to have a method like get_all_models
        models = self.user_repository.get_all_models()
        return models

