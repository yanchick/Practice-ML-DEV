from typing import List
from model.user import User, Transaction, Model
from schema.model_schema import ModelInfo, Balance, Transaction as TransactionSchema
from core.exceptions import ValidationError
from core.security import verify_password
from services.predict_service import PredictService
from core.exceptions import DuplicatedError
from repository.model_repository import ModelRepository
from repository.user_repository import UserRepository

class BillingService:
    def __init__(
        self,
        user_repository: UserRepository,
        predict_service: PredictService,
        model_repository: ModelRepository
    ):
        self.user_repository = user_repository
        self.predict_service = predict_service
        self.model_repository = model_repository

    def purchase_model(self, user: User, model_name: str):
        model_tokens_mapping = {
            "LR": 5,
            "SVM": 10,
            "Catboost": 15,
        }

        # Check if the model exists
        if model_name not in model_tokens_mapping:
            raise ValidationError(detail="Invalid model name")

        model_price = model_tokens_mapping[model_name]

        # Check if the user has sufficient balance
        if user.balance < model_price:
            raise ValidationError(detail="Insufficient funds")

        try:
            # Deduct tokens from the user's balance
            user.balance -= model_price

            # Commit the balance update to the database
            self.user_repository.commit()

            # Create a transaction record
            transaction = Transaction(
                user_id=user.user_id,
                amount=model_price,
                status="completed",  # Adjust the status based on your requirements
            )
            self.user_repository.create(transaction)

            # Run the prediction for the purchased model
            result = self.predict_service.run_model(user, model_name)

            # If the prediction is successful, return the result
            return result
        except Exception as e:
            # If there's an error, rollback the balance update and re-raise the exception
            user.balance += model_price
            self.user_repository.rollback()
            raise e

    def get_available_models(self) -> List[ModelInfo]:
        # Implement the logic to get available models directly using BaseRepository
        # You can modify BaseRepository to have a method like get_all_models
        models = self.user_repository.get_all_models()
        return [ModelInfo(model_id=model.id, description=model.description, price=model.price) for model in models]

    def get_user_balance(self, user: User) -> Balance:
        return Balance(balance=user.balance)

    def get_user_transaction_history(self, user: User) -> List[TransactionSchema]:
        transactions = self.user_repository.get_transactions_by_user(user.user_id)
        return [TransactionSchema(transaction_id=transaction.id, amount=transaction.amount, timestamp=transaction.timestamp) for transaction in transactions]

    def choose_model(self, user: User, modelid: int):
        # Check if the model exists
        model = self.model_repository.get_model_by_id(modelid)
        if not model:
            raise ValidationError(detail=f"Model with id {modelid} does not exist")

        # Update the user's chosen model
        user.chosen_model_id = modelid

        try:
            # Commit the user update to the database
            self.user_repository.commit()
        except Exception as e:
            # Handle any errors that occur during the commit
            raise ValidationError(detail="Failed to choose the model") from e



