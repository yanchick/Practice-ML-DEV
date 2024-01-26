from datetime import datetime
#from typing import List, Optional
from sqlmodel import Field, Text
from  model.base_model import BaseModel
from model.model import Model
from model.user import User
from model.prediction import Prediction
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Transaction(BaseModel, table=True):
    #transaction_id = Column(Integer, primary_key=True)
    datetime: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(ForeignKey('user.id'), nullable=False)
    amount: float = Field(default=None, nullable=False)
   # model_id: int = Field Column(Integer, ForeignKey('model.id'), nullable=False)
    model: int = Field(foreign_keys=[Model.name])
    status: str = Field(default=None, nullable=True)
    user: int = Field(foreign_keys=[User.name])
    prediction: int = Field(foreign_keys=[Prediction.name])
    #user = relationship('User', back_populates='Transactions')
    #prediction = relationship('Prediction', back_populates='Transaction')
