# model/predictor.py
from datetime import datetime
from sqlmodel import Column, DateTime, Field, SQLModel, func, String

class Predictor(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    predicted_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    predictor: str = Field(sa_column=Column(String), foreign_keys=[Predictor.name])
    input_data: str = Field(sa_column=Column(String))
    output_data: str = Field(sa_column=Column(String))


from celery import Celery
from model.predictor import Predictor

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def predict_task(model_name, data):
    # Use the Predictor model or perform other Celery tasks here
    return run_prediction(model_name, data)

