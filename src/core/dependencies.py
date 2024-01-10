from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import ValidationError
from services.model_service import ModelService
from  core.config import configs
from  core.container import Container
from  core.exceptions import AuthError
from  core.security import ALGORITHM, JWTBearer
from core.database import get_session
from  model.user import User
from  schema.auth_schema import Payload
from  services.user_service import UserService
from repository.user_repository import UserRepository


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user

def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)
def get_model_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> ModelService:
    return ModelService(user_repository=user_repository)
