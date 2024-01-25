from src.infrastructure.repository.base_repository import SQLAlchemyRepository
from src.infrastructure.database.model import Users


class UserRepository(SQLAlchemyRepository):
    model = Users
