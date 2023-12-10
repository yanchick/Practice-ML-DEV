from typing import List, Optional

from pydantic import BaseModel, EmailStr, SecretStr

from src.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from src.util.schema import AllOptional


class User(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    email__eq: str
    ...


class UpsertUser(BaseUser, metaclass=AllOptional):
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
