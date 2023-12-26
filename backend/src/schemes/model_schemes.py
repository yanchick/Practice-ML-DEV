from pydantic import BaseModel


class PredictionRequestItem(BaseModel):
    name: str


class PredictionRequest(BaseModel):
    predictions: list[PredictionRequestItem]
    model_id: int
