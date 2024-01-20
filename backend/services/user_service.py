from backend.repository.user_repository import UserRepository
from backend.schema.auth_schema import Payload, Session
from backend.schema.user_schema import BaseUser
from backend.services.base_service import BaseService
from backend.utils.date import get_now


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)

    def get_user_by_id(self, user_id: int):
        user = self._repository.read_by_id(user_id)
        if user:
            return BaseUser(
                payload=Payload(id=user.id, email=user.email, name=user.name, is_superuser=user.is_superuser),
                session=Session(access_token='', expiration=get_now()))
        return None

    def update_last_activity(self, user_id: int):
        self._repository.update_last_activity(user_id)

    def get_users_report(self):
        data = self._repository.get_users_report()
        return data
