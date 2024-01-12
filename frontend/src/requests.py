from src import api_client
from src.api_client import AuthenticatedClient, Client
from src.api_client.models import (
    AvailableModels,
    BodyLoginV1UserLoginPost,
    ModelScheme,
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
    token: str

    def login(self, username: str, password: str) -> bool:
        with Client(base_url=self.settings.api_url) as client:
            response = api_client.user.login(
                client=client, body=BodyLoginV1UserLoginPost(username=username, password=password)
            )
            if response.status_code == 200 and response.parsed is not None:
                self.token = response.parsed.access_token
                return True
            return False

    def signup(self, username: str, password: str) -> bool:
        with Client(base_url=self.settings.api_url) as client:
            response = api_client.user.signup(client=client, body=SingUpRequest(username=username, password=password))
            if response.status_code == 200 and response.parsed is not None:
                self.token = response.parsed.access_token
                return True
            return False

    def me(self) -> UserScheme | None:
        with AuthenticatedClient(base_url=self.settings.api_url, token=self.token) as client:
            response = api_client.user.me(client=client)
            if response.status_code == 200:
                return response.parsed
            return None

    def get_user_predictions(self) -> PredictionScheme | None:
        with AuthenticatedClient(base_url=self.settings.api_url, token=self.token) as client:
            response = api_client.prediction.get_user_predictions(client=client)
            return response.parsed

    def get_user_prediction_by_id(self, prediction_id: int) -> PredictionScheme | None:
        with AuthenticatedClient(base_url=self.settings.api_url, token=self.token) as client:
            response = api_client.prediction.get_user_prediction_by_id(client=client, prediction_id=prediction_id)
            return response.parsed

    def post_prediction(self, data: list[str], model_name: str) -> bool:
        model_name_send = AvailableModels.BASE
        match model_name:
            case AvailableModels.BASE:
                model_name_send = AvailableModels.BASE
            case AvailableModels.CATBOOST:
                model_name_send = AvailableModels.CATBOOST
            case AvailableModels.LOGREG_TFIDF:
                model_name_send = AvailableModels.LOGREG_TFIDF
        with AuthenticatedClient(base_url=self.settings.api_url, token=self.token) as client:
            response = api_client.prediction.post_prediction(
                client=client, body=RequestPrediction(data=data), model_name=model_name_send
            )
            if response.status_code == 200:
                return True
            return False

    def get_models(self) -> list[ModelScheme]:
        with Client(base_url=self.settings.api_url) as client:
            response = api_client.model.get_models(client=client)
            return response.parsed.models  # type: ignore


api = Requests()
