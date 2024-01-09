from .base import Base  # Adjust the import based on the location of your `base.py` file
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from pydantic import BaseModel as SQLModel, Field

class BaseModel(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    amount = Column(Float, nullable=False)
    model_id = Column(Integer, ForeignKey('models.model_id'), nullable=False)
    status = Column(String)  
    user = relationship('User', back_populates='transactions')
    prediction = relationship('Prediction', uselist=False, back_populates='transaction')

class Model(Base):
    __tablename__ = 'models'
    model_id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    pickle_file_path = Column(String, nullable=False)
    transactions = relationship('Transaction', back_populates='model')
    predictions = relationship('Prediction', back_populates='model')
