from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class SingUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class UserScheme(BaseModel):
    username: str
    balance: float


class PredictionItem(BaseModel):
    id: int
    predicted_model_id: int
    result: int | None
    input_data: str


class PredictionScheme(BaseModel):
    predictions: list[PredictionItem]


class ModelScheme(BaseModel):
    id: int
    name: str
    description: str
    cost: float


class ModelListScheme(BaseModel):
    models: list[ModelScheme]


class Token(BaseModel):
    access_token: str
    token_type: str