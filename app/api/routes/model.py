from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import model_service
from models import user as user_model
from services import user_service


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

@router.post("/test_model/{user_id}")
def trigger_inference(user_id: str, model_id: int, input_data: str, db: Session = Depends(get_db)):
    try:
        # Enqueue the inference task
        result = perform_inference.apply_async(args=[user_id, model_id, input_data])
        print(result)
        result = str(result)
        # You can return the task ID or any other information to the user
        # model_servic  e.write_action(db, user_id, model_id, result)
        user_service.update_credits(db, user_id, -10)
        return f'task_id: {result}, status: OK'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enqueue inference task: {str(e)}")


@router.post("/action")
def register_user(user_id, model_id, result, db: Session = Depends(get_db)):
    return model_service.write_action(db, user_id, model_id, result)
