from celery import Celery
from services.predict_service import PredictService
from model.user import User
from model.base_model import Model
from schema.model_schema import ModelInfo

app = Celery('tasks', broker='redis://localhost:6379/0')

predict_service = PredictService()

@app.task
def predict_task(model_name: str, input_data: dict, current_user_data: dict):
    current_user = User(**current_user_data)
    
    # Fetch the model details using the model_name
    model_info = Model.get_model_by_name(model_name)
    if not model_info:
        # Handle the case where the model is not found
        return

    # Perform the prediction using the model_info and input_data
    prediction_result = predict_service.run_model(current_user, model_info, input_data)

    # You can further process the prediction_result or store it as needed

