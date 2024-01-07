"""API schema for ML app."""

from pydantic import BaseModel
from datetime import datetime
from enum import IntEnum


class Balance(BaseModel):
    """User account balance."""

    balance: int
    frozen: int
    raw_balance: int


class JobStatus(IntEnum):
    """Job status."""

    pending = 1
    completed = 2
    failed = 3


class Job(BaseModel):
    """Computation executed in the service."""

    status: JobStatus
    cost: int
    created_at: datetime
    result: list[any]


class LearnModel(BaseModel):
    """Model that can be run in a job."""

    id: int
    description: str
    cost: int
