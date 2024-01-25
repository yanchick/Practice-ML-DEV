from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPBearer
from jose import JWTError, jwt

from src.api.schemas.auth_schema import User
from src.infrastructure.core.exceptions import CredentialsError

SECRET_KEY = "THIS_IS_A_SECRET_KEY"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()


def create_jwt_token(user: User) -> str:
    data = user.model_dump()

    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise CredentialsError


def get_current_user(token: str = Depends(bearer_scheme)) -> User:
    token = token.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        import logging as log
        log.warning(payload)
        username: str = payload.get("username")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise CredentialsError

    except JWTError:
        raise CredentialsError

    return User(id=user_id,
                username=username)
