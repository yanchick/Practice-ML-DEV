from sqlalchemy import ForeignKey, Integer
from sqlmodel import Column, Field, Relationship, SQLModel


class Prediction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    merchant_id: int = Field()
    cluster_id: int = Field()
    category_id: int = Field()
    batch_id: int = Field(sa_column=Column(Integer, ForeignKey("predictionbatch.id")))
    batch: "PredictionBatch" = Relationship(back_populates="predictions")
