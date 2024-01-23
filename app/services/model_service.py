from sqlalchemy.orm import Session
from database import service
from models import UserResponse

def get_models(db: Session):
    return service.get_models(db)

def run_model(db: Session, user_id: int, model_id: int):
    pass
    # return service.create_user(db, user)