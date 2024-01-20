from datetime import datetime

from pydantic import BaseModel, Field

from backend.utils.date import get_now


class DepositRequest(BaseModel):
    amount: int = Field(..., gt=0, description="The amount to be deposited. Must be greater than 0.")


class TransactionInfo(BaseModel):
    id: int = Field(..., description="Unique identifier for the transaction.")
    amount: int = Field(..., description="The transaction amount.")
    timestamp: datetime = Field(default_factory=get_now(), description="Timestamp of the transaction.")


class CreditsReport(BaseModel):
    total_credits_purchased: int = Field(..., description="Total amount of credits purchased by users.")
    total_credits_spent: int = Field(..., description="Total amount of credits spent by users.")
