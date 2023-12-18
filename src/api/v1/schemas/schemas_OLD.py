from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Billing(BaseModel):
    coins: int

class Prediction(BaseModel):
    lifespan: float

class ActionsHistory(BaseModel):
    ID: int
    Type: str
    CoinsDiff: int
    Description: str
    Time: str
