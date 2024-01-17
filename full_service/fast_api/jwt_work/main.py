import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends

import secrets


class JWT_worker:
    def __init__(self):
        self.SECRET_KEY = self.generate_secret_key()
        self.ALGORITHM = "HS256"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def generate_secret_key(self, length: int = 32) -> str:
        return secrets.token_urlsafe(length)

    def create_access_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_jwt

    def get_current_user(self, token: str):
        if token is None:
            token = Depends(self.oauth2_scheme)
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception
        except Exception:
            raise credentials_exception
        return username
