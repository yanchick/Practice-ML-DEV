from sqlmodel import Field, Relationship

from backend.model.base_model import BaseModel


class Transaction(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    amount: int = Field()
    prediction_batch: "PredictionBatch" = Relationship(back_populates="transaction")
