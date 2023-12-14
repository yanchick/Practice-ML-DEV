from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Billing(BaseModel):
    coins: int

class ActionsHistory(BaseModel):
    ID: int
    Type: str
    CoinsDiff: int
    Description: str
    Time: str
