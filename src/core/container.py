from dependency_injector import containers, providers

from core.config import configs
from core.database import Database
from repository.user_repository import UserRepository
from repository.model_repository import ModelRepository
from services.user_service import UserService
from services.auth_service import AuthService
from services.predict_service import PredictService
from services.billing_service import BillingService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.endpoints.auth",
            "core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    model_repository = providers.Factory(ModelRepository, session_factory=db.provided.session)
    user_service = providers.Factory(UserService, user_repository=user_repository)

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    predict_service = providers.Factory(PredictService)

    billing_service = providers.Factory(BillingService, user_repository=user_repository, predict_service=predict_service)