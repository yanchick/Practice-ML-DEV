from service.api.repositories.base import SQLAlchemyRepository
from service.api.models import DBUser

class UserRepository(SQLAlchemyRepository):
    model = DBUser
