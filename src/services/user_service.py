from model.user import User
from core.exceptions import ValidationError
from repository.user_repository import UserRepository
from services.base_service import BaseService

class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_user_balance(self, user: User):
        return self.user_repository.get_user_balance(user)

    def get_user_transaction_history(self, user: User):
        return self.user_repository.get_user_transaction_history(user)

