from typing import List

from pydantic import BaseModel


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


class HealthResponse(BaseModel):
    description: str = "I am alive"


# class UnauthorizedResponse(BaseModel):
#     description: str = "App token is not valid"


# class NotFoundResponse(BaseModel):
#     description: str = "Model or user not found"
