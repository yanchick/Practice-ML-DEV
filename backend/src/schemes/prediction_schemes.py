from pydantic import BaseModel, Field


class RequestPrediction(BaseModel):
    data: list[str] = Field(..., min_length=1, max_items=100)
