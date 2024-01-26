from datetime import datetime
from typing import ClassVar
#import predictor
from model.model import Model
#from model.transanction import Transanction
from model.user import User
from model.base_model import BaseModel
from sqlmodel import Column, String, DateTime, Field, SQLModel, func #uuid


class Prediction(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    predicted_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    user: str = Field(sa_column=Column(String), foreign_key='User.name')
    #predictor: str = Field(sa_column=Column(String), foreign_keys=[Predictor.name])
    model: str = Field(sa_column=Column(String), foreign_keys=[Model.name])
    #transanction: int = Field(sa_column=Column(String), foreign_keys=[Transanction.id])
    #user: str = Field(sa_column=Column(String), foreign_keys=[User.name])
    input_data: str = Field(sa_column=Column(String))
    output_data: str = Field(sa_column=Column(String))
