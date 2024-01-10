from typing import List, Dict, Any
from model.base_model import Model
from model.user import User
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

    def choose_model(self, user: User, model_id: int):
        self.user_repository.choose_model(user, model_id)

    def upload_data(self, current_user: User, data: Dict[str, Any]):
        # Check if the user has a chosen model
        chosen_model_id = current_user.chosen_model_id
        if not chosen_model_id:
            raise ValueError("User has not chosen any model")

        # Store the uploaded data temporarily in the user's chosen model
        current_user.temp_uploaded_data = data

        # Commit the changes to the database
        try:
            self.user_repository.commit()
            print(f"Data uploaded for model {model_id} by user {current_user.id}")
        except Exception as e:
            # Handle any errors that occur during the commit
            raise ValueError(f"Failed to upload data: {str(e)}")

