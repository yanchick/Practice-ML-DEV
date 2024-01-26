from datetime import datetime
#from typing import List, Optional
from sqlmodel import Field, Text
from  model.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



class Model(BaseModel):
    name: str = Field(default=None, nullable=True)
    status: str = Field(default=None, nullable=True)
    description: str = Field()
    price: int = Field(default=None, nullable=True)
    pickle_file_path: str = Field(default=None, nullable=True)
    #transactions = relationship('Transaction', back_populates='model')
    #predictions = relationship('Prediction', back_populates='model')
