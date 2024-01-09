from datetime import datetime

from pydantic import BaseModel

from .user_schema import User


class SignIn(BaseModel):
    email__eq: str
    password: str


class SignUp(BaseModel):
    email: str
    password: str
    name: str


class Payload(BaseModel):
    id: int
    email: str
    name: str
    is_superuser: bool

    #class Config:
        #arbitrary_types_allowed = True
        #from_attributes = True


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User

    class Config:
        from_attributes = True
        model_config = {'protected_namespaces': ()}


