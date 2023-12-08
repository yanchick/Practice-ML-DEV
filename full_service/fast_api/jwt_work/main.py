import jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends

import secrets

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


class JWT_worker:
    def __init__(self):
        self.SECRET_KEY = self.generate_secret_key()
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
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.JWTError:
            raise credentials_exception
        return username
