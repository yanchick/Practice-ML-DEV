from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


class UserLogin(BaseModel):
    name: str
    password: str


class UserRegister(BaseModel):
    email: str
    password: str
    name: str


class UserLoginResponse(BaseModel):
    access_token: str
    #expiration: datetime
    user_info: User


class Payload(BaseModel):
    id: int
    email: str
    name: str
