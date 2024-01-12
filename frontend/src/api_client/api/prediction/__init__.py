from .get_prediction_v1_prediction_predict_prediction_id_get import sync_detailed as get_user_prediction_by_id
from .get_user_predictions_v1_prediction_get import sync_detailed as get_user_predictions
from .predict_v1_prediction_predict_post import sync_detailed as post_prediction

__all__ = [
    "get_user_predictions",
    "get_user_prediction_by_id",
    "post_prediction",
]
