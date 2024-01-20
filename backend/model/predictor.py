from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Predictor(SQLModel, table=True):
    name: str = Field(unique=True, primary_key=True)
    cost: int = Field()
    prediction_batches: List["PredictionBatch"] = Relationship(back_populates="predictor")
