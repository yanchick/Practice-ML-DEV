from sqlalchemy.orm import Session, joinedload
from database import User, Action, Model

def create_user(db: Session, user_data: User):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_models(db: Session):
    return db.query(Model).all()

def get_user_actions(db: Session, user_id: int):
    return (
        db.query(Action)
        .options(joinedload(Action.user), joinedload(Action.model))
        .filter(Action.user_id == user_id)
        .all()
    )

def add_user_credits(db: Session, user_id: int, new_credits: int):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.credits = db_user.credits + new_credits
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def substruct_user_credits(db: Session, user_id: int, spent_credits: int):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.credits = db_user.credits - spent_credits
        db.commit()
        db.refresh(db_user)
        return db_user
    return None