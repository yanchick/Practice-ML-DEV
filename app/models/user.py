from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    username: str
    credits: int
    
class ModelsResponse(BaseModel):
    name: str

class ActionsResponse(BaseModel):
    user: str
    model: int
    time: datetime
    data: str
    
class ModelsResponse(BaseModel):
    id: int
    name: str
    cost: int
    