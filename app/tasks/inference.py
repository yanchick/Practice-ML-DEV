# tasks/inference.py

from celery import Celery
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
# from database import get_db
# from database.models import Model
# from services import model_service

celery = Celery('tasks', broker=os.getenv('BROKER_URL'))

@celery.task
def perform_inference(model_id: int, input_data: dict):
    # db = next(get_db())
    # model = model_service.get_model(db, model_id)
    # if model is None:
    #     raise HTTPException(status_code=404, detail=f"Model {model_id} not found")
    pass

# TODO: inference the models
    # Perform inference using the model and input_data
    # Example: result = some_inference_function(model, input_data)

    # Return or save the inference result
    # return {"model_id": model_id, "inference_result": result}
