from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

class SignInResponse(BaseModel):
    access_token: str
    user_info: User

class PredictionResponce(BaseModel):
    is_anomaly: bool
    anomaly_probability: float
    



