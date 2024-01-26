from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import user_service
from models import user as user_model

router = APIRouter(prefix="/user")

@router.post("/")
def register_user(user: user_model.UserResponse, db: Session = Depends(get_db)):
    return user_service.register_user(db, user)

@router.get("/{user_id}", response_model=user_model.UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/", response_model=user_model.UserResponse)
def update_user_credits(user_id: str, new_credits: int, db: Session = Depends(get_db)):
    db_user = user_service.update_credits(db, user_id, new_credits)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/model/{user_id}/", response_model=user_model.UserResponse)
def update_user_credits(user_id: str, new_credits: int, db: Session = Depends(get_db)):
    db_user = user_service.update_credits(db, user_id, new_credits)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/actions/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user_action = user_service.get_user_actions(db, user_id)
    if db_user_action is None:
        raise HTTPException(status_code=404, detail="User actions not found")
    return db_user_action