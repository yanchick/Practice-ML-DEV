from redis import Redis
from rq import Queue
from .queue_work.queue_functions import (
    process_response,
)


class Inference_handler:
    def __init__(self, inference_server_url="http://127.0.0.1:8936"):
        self.inference_server_url = inference_server_url
        self.predict_url = f"{self.inference_server_url}/predict"
        self.redisq = Queue(connection=Redis())

    def _check_data(
        self,
        model,
        age,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
    ):
        error_responce = "Invalid data"
        model = model
        age = 0 if len(age) == 0 else 1
        if gender:
            gender = 0 if gender == "male" else 1
        else:
            return error_responce
        if sport_days:
            sport_days = sport_days
        else:
            return error_responce
        if bmi:
            bmi = bmi
        else:
            return error_responce
        if glucose:
            glucose = glucose
        else:
            return error_responce
        if diabetes_degree:
            diabetes_degree = diabetes_degree
        else:
            return error_responce
        if hemoglobin:
            hemoglobin = hemoglobin
        else:
            return error_responce
        if insulin:
            insulin = insulin
        else:
            return error_responce
        return (
            model,
            age,
            gender,
            sport_days,
            bmi,
            glucose,
            diabetes_degree,
            hemoglobin,
            insulin,
        )

    def predict(
        self,
        user_id,
        model,
        age,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
    ):
        checked_data = self._check_data(
            model,
            age,
            gender,
            sport_days,
            bmi,
            glucose,
            diabetes_degree,
            hemoglobin,
            insulin,
        )
        if checked_data == "Invalid data":
            return None
        else:
            data = {
                "model": checked_data[0],
                "age_group": checked_data[1],
                "RIAGENDR": checked_data[2],
                "PAQ605": checked_data[3],
                "BMXBMI": checked_data[4],
                "LBXGLU": checked_data[5],
                "DIQ010": checked_data[6],
                "LBXGLT": checked_data[7],
                "LBXIN": checked_data[8],
            }
            res = process_response.delay(self.predict_url, data, user_id)

            return res
