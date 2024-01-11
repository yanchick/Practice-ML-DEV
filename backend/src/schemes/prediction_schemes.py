from pydantic import BaseModel, Field


class RequestPrediction(BaseModel):
    data: list[str] = Field(..., min_length=1)
