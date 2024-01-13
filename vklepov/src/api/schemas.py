"""API schema for ML app."""

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import IntEnum
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class Balance(BaseModel):
    """User account balance."""

    balance: int


class Deposit(BaseModel):
    amount: int


class JobStatus(IntEnum):
    """Job status."""

    pending = 1
    completed = 2
    failed = 3


class JobShort(BaseModel):
    """Computation executed in the service."""

    id: int
    status: JobStatus
    cost: int
    created_at: datetime


class Job(JobShort):
    """Computation executed in the service, including result."""

    result: Optional[any]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class LearnModel(BaseModel):
    """Model that can be run in a job."""

    id: int
    description: str
    cost: int
