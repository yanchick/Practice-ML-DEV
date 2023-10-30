from sqlmodel import Field

from  model.base_model import BaseModel


class Predictor(BaseModel, table=false):
    name: str = Field(unique=True)
    cost: int = Field()
    is_active: bool = Field(default=True)
