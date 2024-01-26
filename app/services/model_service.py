from sqlalchemy.orm import Session
from database import service
from models import UserResponse
from datetime import datetime 

def get_models(db: Session):
    return service.get_models(db)

def write_action(db: Session, user_id: int, model_id: int, result: str):
    return service.save_action(db, user_id, model_id, datetime.now(), result)
