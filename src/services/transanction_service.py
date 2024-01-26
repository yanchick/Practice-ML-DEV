from model.user import User
from model.base_model import Transaction
from core.exceptions import ValidationError
from repository.user_repository import UserRepository
from services.base_service import BaseService

class TransactionService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def create_transaction(self, user: User, amount: float, model_id: int):
        try:
            # Deduct tokens from the user's balance
            user.balance -= amount

            # Commit the balance update to the database
            self.user_repository.commit()

            # Create a transaction record
            transaction = Transaction(
                user_id=user.user_id,
                amount=amount,
                model_id=model_id,
                status="completed",  # Adjust the status based on your requirements
            )
            self.user_repository.create(transaction)

            return transaction
        except Exception as e:
            # If there's an error, rollback the balance update and re-raise the exception
            user.balance += amount
            self.user_repository.rollback()
            raise e

