from dependency_injector import containers, providers

from backend.core.config import configs
from backend.core.database import Database
from backend.repository.predictor_repository import PredictorRepository
from backend.repository.billing_repository import BillingRepository
from backend.repository.prediction_repository import PredictionRepository
from backend.repository.user_repository import UserRepository
from backend.services.auth_service import AuthService
from backend.services.billing_service import BillingService
from backend.services.prediction_service import PredictionService
from backend.services.predictor_service import PredictorService
from backend.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "backend.api.v1.endpoints.admin",
            "backend.api.v1.endpoints.auth",
            "backend.api.v1.endpoints.billing",
            "backend.api.v1.endpoints.prediction",
            "backend.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    billing_repository = providers.Factory(BillingRepository, session_factory=db.provided.session)
    prediction_repository = providers.Factory(PredictionRepository, session_factory=db.provided.session)
    predictor_repository = providers.Factory(PredictorRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    billing_service = providers.Factory(BillingService, billing_repository=billing_repository)
    predictor_service = providers.Factory(PredictorService, predictor_repository=predictor_repository)
    prediction_service = providers.Factory(PredictionService, prediction_repository=prediction_repository)
