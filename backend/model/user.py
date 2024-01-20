from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship

from backend.model.base_model import BaseModel


class User(BaseModel, table=True):
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    password: str = Field()
    name: Optional[str] = Field(default=None, nullable=True)
    is_superuser: bool = Field(default=False)
    last_activity_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now()))
    balance: int = Field(default=0)
    reserved_funds: int = Field(default=0)
    prediction_batches: List["PredictionBatch"] = Relationship(back_populates="user")
