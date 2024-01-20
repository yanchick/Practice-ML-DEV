from typing import List

from backend.core.celery_worker import async_make_batch_predictions
from backend.repository.prediction_repository import PredictionRepository
from backend.schema.prediction_schema import PredictionBatchInfo, PredictionInfo
from backend.schema.prediction_schema import PredictionFeatures, PredictionTarget, PredictionsReport
from backend.services.base_service import BaseService

_CATEGORY_LABEL_MAP = {
    2612: "Mobile Phones",
    2614: "TVs",
    2615: "CPUs",
    2617: "Digital Cameras",
    2618: "Microwaves",
    2619: "Dishwashers",
    2620: "Washing Machines",
    2621: "Freezers",
    2622: "Fridge Freezers",
    2623: "Fridges"
}


def make_prediction(model, merchant_id: int, cluster_id: int):
    input_data = [merchant_id, cluster_id]
    category_id = model.predict([input_data])[0]
    category_label = _CATEGORY_LABEL_MAP.get(category_id, "Unknown Category")
    return {"merchant_id": merchant_id, "cluster_id": cluster_id, "category_id": category_id,
            "category_label": category_label}


class PredictionService(BaseService):

    def __init__(self, prediction_repository: PredictionRepository):
        super().__init__(prediction_repository)
        self.prediction_repository = prediction_repository

    @staticmethod
    def make_batch_prediction(model_name, prediction_requests: List[dict]):
        async_result = async_make_batch_predictions.delay(model_name, prediction_requests)
        return async_result

    def save_batch_prediction(self, user_id: int, model_name: str, transaction_id: int, prediction_results: List[dict]):
        batch = self.prediction_repository.create_batch(user_id=user_id, predictor_name=model_name,
                                                        transaction_id=transaction_id)
        for result in prediction_results:
            prediction_data = {
                'batch_id': batch.id,
                'merchant_id': result['merchant_id'],
                'cluster_id': result['cluster_id'],
                'category_id': result['category_id'],
            }
            self.prediction_repository.create_prediction(prediction_data)
        return batch

    def get_prediction_history(self, user_id: int) -> List[PredictionBatchInfo]:
        prediction_batches = self.prediction_repository.get_prediction_history(user_id)
        result = []

        for batch in prediction_batches:
            prediction_infos = []
            for prediction in batch.predictions:
                category_label = _CATEGORY_LABEL_MAP.get(prediction.category_id, "Unknown Category")
                prediction_info = PredictionInfo(
                    features=PredictionFeatures(
                        merchant_id=prediction.merchant_id,
                        cluster_id=prediction.cluster_id
                    ),
                    target=PredictionTarget(
                        category_id=prediction.category_id,
                        category_label=category_label
                    )
                )
                prediction_infos.append(prediction_info)

            model_name = batch.predictor.name
            transaction_amount = batch.transaction.amount if batch.transaction else 0
            timestamp = batch.created_at

            prediction_batch_info = PredictionBatchInfo(
                id=batch.id,
                predictions=prediction_infos,
                model_name=model_name,
                cost=transaction_amount,
                timestamp=timestamp
            )
            result.append(prediction_batch_info)

        return result

    def get_predictions_reports(self):
        raw_reports = self.prediction_repository.get_predictions_reports()
        predictions_reports = [PredictionsReport(model_name=model_name, total_prediction_batches=total_predictions)
                               for model_name, total_predictions in raw_reports]
        return predictions_reports
