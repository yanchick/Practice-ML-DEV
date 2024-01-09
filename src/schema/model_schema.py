# schema/model_schema.py
from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    transaction_id: int
    amount: float
    timestamp: datetime

class Balance(BaseModel):
    balance: float

class ModelInfo(BaseModel):
    modelid: int
    description: str
    price: float

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}



