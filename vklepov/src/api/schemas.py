"""API schema for ML app."""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import IntEnum


class Balance(BaseModel):
    """User account balance."""

    balance: int


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

    model_config = ConfigDict(arbitrary_types_allowed=True)


class JobCreate(BaseModel):
    model_id: int


class LearnModel(BaseModel):
    """Model that can be run in a job."""

    id: int
    description: str
    cost: int
