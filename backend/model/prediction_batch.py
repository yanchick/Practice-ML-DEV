from typing import List

from sqlalchemy import Integer, Column, ForeignKey, String
from sqlmodel import Relationship, Field

from backend.model.base_model import BaseModel


class PredictionBatch(BaseModel, table=True):
    id: int = Field(primary_key=True)
    predictor_name: str = Field(sa_column=Column(String, ForeignKey("predictor.name")))
    predictor: "Predictor" = Relationship(back_populates="prediction_batches")
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("user.id")))
    user: "User" = Relationship(back_populates="prediction_batches")
    transaction_id: int = Field(sa_column=Column(Integer, ForeignKey("transaction.id")))
    transaction: "Transaction" = Relationship(back_populates="prediction_batch")
    predictions: List["Prediction"] = Relationship(back_populates="batch")
