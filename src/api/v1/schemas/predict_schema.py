from pydantic import BaseModel


class PredictionResponce(BaseModel):
    lifespan: float
