import requests
from redis import Redis
from rq.decorators import job
from rq import Callback
from rq import get_current_job


def add_prediction_row_from_queue(job, connection, result, *args, **kwargs):
    register_url = "http://127.0.0.1:8935/add_row"
    data_to_send = job.get_meta().copy()
    data_to_send["result"] = result
    requests.post(register_url, json=data_to_send)


@job(
    "high",
    connection=Redis(),
    on_success=Callback(add_prediction_row_from_queue),
)
def process_response(url, data, user_id):
    cur_job = get_current_job()
    cur_job.meta = {
        "user_id": user_id,
        "model": data["model"],
        "age_group": data["age_group"],
        "gender": data["RIAGENDR"],
        "sport_days": data["PAQ605"],
        "bmi": data["BMXBMI"],
        "glucose": data["LBXGLU"],
        "diabetes_degree": data["DIQ010"],
        "hemoglobin": data["LBXGLT"],
        "insulin": data["LBXIN"],
    }
    cur_job.save_meta()
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["prediction"][0]
    else:
        return None
