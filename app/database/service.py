from sqlalchemy.orm import Session, joinedload
from database import User, Action, Model
import json

def create_user(db: Session, user_data: User):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_models(db: Session):
    return db.query(Model).all()


def get_user_actions(db: Session, user_id: str):
    return (
        db.query(Action)
        .options(joinedload(Action.user), joinedload(Action.model))
        .filter(Action.user_id == user_id)
        .all()
    )


def update_credits(db: Session, user_id: str, spent_credits: int):
    db_user = get_user(db, user_id)
    if db_user:
        if db_user.credits + spent_credits <= 0:
            return None
        db_user.credits = db_user.credits + spent_credits
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def save_action(db: Session, user_id: str, model_id: int, timestamp, result: str):
    print(user_id, model_id, timestamp, result)
    db_action = Action(user_id=user_id, model_id=model_id, timestamp=timestamp, data=str(result))
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action