from src.infrastructure.repository.base_repository import SQLAlchemyRepository
from src.infrastructure.database.model import Models


class ModelsRepository(SQLAlchemyRepository):
    model = Models
