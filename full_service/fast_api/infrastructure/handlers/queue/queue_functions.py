import requests
from redis import Redis
from rq import Queue, Retry
from ...database.database_functions import add_predict_row


def process_response(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["prediction"][0]
    else:
        return None


# def add_prediction_row_from_queue(job, connection, result, *args, **kwargs):
#     data = kwargs["data"]
#     user_id = kwargs["user_id"]
#     add_predict_row(
#         user_id=user_id,
#         model=data["model"],
#         age_group=data["age_group"],
#         gender=data["gender"],
#         sport_days=data["sport_days"],
#         bmi=data["bmi"],
#         glucose=data["glucose"],
#         diabetes_degree=data["diabetes_degree"],
#         hemoglobin=data["hemoglobin"],
#         insulin=data["insulin"],
#         result=job.return_value(),
#     )
