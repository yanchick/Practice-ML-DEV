from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    credits: int
    
class ModelsResponse(BaseModel):
    name: str

class ActionsResponse(BaseModel):
    model: str
    user: int
    time: datetime
    
class ModelsResponse(BaseModel):
    id: int
    name: str
    cost: int
    