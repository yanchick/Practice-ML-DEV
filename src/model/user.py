from sqlmodel import Field, Text

from  model.base_model import BaseModel

class User(BaseModel, table=True):
    email: str = Text()
    password: str = Text()
    #user_token: str = Field(unique=True)
    #blance: int = Field(default=500)
    #name: str = Field(default=None, nullable=True)
    #is_active: bool = Field(default=True)
    #is_superuser: bool = Field(default=False)
    #predictions: list = Field(default=None, nullable=True)