from src import api_client
from src.api_client import AuthenticatedClient, Client
from src.api_client.models import (
    AvailableModels,
    BodyLoginV1UserLoginPost,
    ModelListScheme,
    PredictionScheme,
    RequestPrediction,
    SingUpRequest,
    UserScheme,
)
from src.settings import Settings


def singleton(class_):  # type: ignore
    instances = {}

    def getinstance(*args, **kwargs):  # type: ignore
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Requests:
    settings = Settings()
    client: Client = Client(base_url=settings.api_url)
    auth_client: AuthenticatedClient

    @classmethod
    def login(cls, username: str, password: str) -> bool:
        with cls.client as client:
            response = api_client.user.login(
                client=client, body=BodyLoginV1UserLoginPost(username=username, password=password)
            )
            if response.status_code == 200 and response.parsed is not None:
                cls.auth_client = AuthenticatedClient(base_url=cls.settings.api_url, token=response.parsed.access_token)
                return True
            return False

    @classmethod
    def signup(cls, username: str, password: str) -> bool:
        with cls.client as client:
            response = api_client.user.signup(client=client, body=SingUpRequest(username=username, password=password))
            if response.status_code == 200 and response.parsed is not None:
                cls.auth_client = AuthenticatedClient(base_url=cls.settings.api_url, token=response.parsed.access_token)
                return True
            return False

    @classmethod
    def me(cls) -> UserScheme | None:
        with cls.auth_client as client:
            response = api_client.user.me(client=client)
            if response.status_code == 200:
                return response.parsed
            return None

    @classmethod
    def get_user_predictions(cls) -> PredictionScheme | None:
        with cls.auth_client as client:
            response = api_client.prediction.get_user_predictions(client=client)
            return response.parsed

    @classmethod
    def get_user_prediction_by_id(cls, prediction_id: int) -> PredictionScheme | None:
        with cls.auth_client as client:
            response = api_client.prediction.get_user_prediction_by_id(client=client, prediction_id=prediction_id)
            return response.parsed

    @classmethod
    def post_prediction(cls, data: list[str], model_name: AvailableModels) -> bool:
        with cls.auth_client as client:
            response = api_client.prediction.post_prediction(
                client=client, body=RequestPrediction(data=data), model_name=model_name
            )
            if response.status_code == 200:
                return True
            return False

    @classmethod
    def get_models(cls) -> ModelListScheme | None:
        with cls.auth_client as client:
            response = api_client.model.get_models(client=client)
            return response.parsed
