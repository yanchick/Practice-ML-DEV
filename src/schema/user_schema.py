from typing import List, Optional

from pydantic import BaseModel

from  schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from  util.schema import AllOptional


class User(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}




class BaseUser(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}


class BaseUserWithPassword(BaseUser):
    password: str

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    email__eq: Optional[str] = None
    email: Optional[str] = None
    user_token: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    ordering: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = None

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}


class UpsertUser(BaseUser, metaclass=AllOptional):
    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}
