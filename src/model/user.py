from datetime import datetime
from typing import List, Optional
from .base import Base
from .base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlmodel import Field, Text, Relationship

class User(BaseModel):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field()
    password: str = Field()
    user_token: str = Field(unique=True)
    balance: int = Field(default=500)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    name: Optional[str] = Field(default=None)

    transactions = Relationship("Transaction", uselist=False, back_populates="user")


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    transaction_id: int = Field(primary_key=True)
    datetime: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(ForeignKey('users.id'))
    amount: float = Field()
    modelid: int = Field(ForeignKey('models.modelid'))
    status: str = Field()

    user = Relationship("User", back_populates="transactions")
    model = Relationship("Model", back_populates="transactions")

class Model(BaseModel):
    __tablename__ = 'models'

    modelid: int = Field(primary_key=True)
    description: str = Field()
    price: float = Field()
    pickle_file_path: str = Field()

    transactions = relationship("Transaction", back_populates="model")
