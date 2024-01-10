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
from model.user import User

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def predict_task(user_id, model_name):
    # Fetch the user and the uploaded data
    user = User.get(id)
    uploaded_data = user.temp_uploaded_data

    # Perform the prediction logic using the model_name and uploaded_data
    prediction_result = run_prediction(model_name, uploaded_data)

    # Update the Predictor model or perform other Celery tasks here
    predictor = Predictor(predictor=model_name, input_data=str(uploaded_data), output_data=str(prediction_result))
    Predictor.save(predictor)

    return prediction_result


