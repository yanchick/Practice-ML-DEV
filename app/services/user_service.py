from sqlalchemy.orm import Session
from database import service
from models import UserResponse

def register_user(db: Session, user: UserResponse):
    return service.create_user(db, user)

def get_user(db: Session, user_id: int):
    return service.get_user(db, user_id)

def get_user_actions(db: Session, user_id: int):
    return service.get_user_actions(db, user_id)

def update_credits(db: Session, user_id: int, credits: int):
    return service.update_credits(db, user_id, credits)