import pickle
from fastapi import HTTPException
from model.user import User
from core.exceptions import ValidationError

class PredictService:
    def run_model(self, user: User, model_name: str, input_data: dict) -> None:
        # Replace this with the actual path where your models are stored
        model_path = f"model/{model_name}.pkl"

        try:
            # Load the model
            with open(model_path, 'rb') as model_file:
                model = pickle.load(model_file)

            # Perform the prediction using the provided input_data
            prediction_result = model.predict(input_data)

            # You can use the prediction_result as needed
            print(f"Prediction Result: {prediction_result}")

            # Return the result or handle it as required
            return prediction_result

        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
        except Exception as e:
            # If there's an error, raise a ValidationError or another appropriate exception
            raise ValidationError(detail=f"Error running prediction: {str(e)}")

