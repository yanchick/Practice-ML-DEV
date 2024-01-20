from pydantic import BaseModel, Field


class PredictorInfo(BaseModel):
    name: str = Field(..., description="Name of the predictor model.")
    cost: int = Field(..., description="Cost associated with using this predictor model.")
