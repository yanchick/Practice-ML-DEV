from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import model_service
from models import user as user_model

from celery import Celery
from celery_config import broker_url
from tasks.inference import perform_inference

router = APIRouter(prefix="/model")

celery = Celery(
    'tasks',
    broker=broker_url,
    include=['tasks.inference'],
)


@router.get("/")
def register_user(db: Session = Depends(get_db)):
    return model_service.get_models(db)
