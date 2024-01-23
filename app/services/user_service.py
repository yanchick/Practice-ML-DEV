from sqlalchemy.orm import Session
from database import service
from models import UserResponse

def register_user(db: Session, user: UserResponse):
    return service.create_user(db, user)

def get_user(db: Session, user_id: int):
    return service.get_user(db, user_id)

def add_credits(db: Session, user_id: int, credits: int):
    return service.add_user_credits(db, user_id, credits)

def substruct_credits(db: Session, user_id: int, credits: int):
    return service.substruct_user_credits(db, user_id, credits)

def run_model(db: Session, user_id: int, model_id: int):
    pass