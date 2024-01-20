import os

from celery import Celery

from backend.core.config import configs

celery = Celery('prediction_worker')

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", configs.BROKER_URL)
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", configs.BROKER_RESULT_BACKEND)

celery.conf.update(
    task_serializer='pickle',
    result_serializer='pickle',
    accept_content=['pickle'],
    worker_send_task_events=True,
    worker_disable_rate_limits=False,
)


@celery.task
def async_make_batch_predictions(model_name, prediction_requests):
    from backend.services.prediction_service import make_prediction
    from backend.services.predictor_service import load_model
    model = load_model(model_name)
    results = []
    for request in prediction_requests:
        results.append(make_prediction(model, request['merchant_id'], request['cluster_id']))
    return results
