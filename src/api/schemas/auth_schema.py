from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    user_info: User


class Balance(BaseModel):
    balance: int
