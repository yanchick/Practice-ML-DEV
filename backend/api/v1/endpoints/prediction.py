from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from backend.core.container import Container
from backend.core.dependencies import get_current_user_payload
from backend.core.exceptions import PredictionError, ValidationError
from backend.schema.auth_schema import Payload
from backend.schema.prediction_schema import PredictionRequest, PredictionBatchInfo, PredictionInfo, \
    PredictionTarget, PredictionFeatures
from backend.schema.predictor_schema import PredictorInfo
from backend.services.billing_service import BillingService
from backend.services.prediction_service import PredictionService
from backend.services.predictor_service import PredictorService
from backend.utils.date import get_now

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
)


@router.get("/models", response_model=List[PredictorInfo])
@inject
async def get_available_models(
        predictor_service: PredictorService = Depends(Provide[Container.predictor_service])
):
    available_models = predictor_service.get_available_models()
    return available_models


@router.get("/history", response_model=List[PredictionBatchInfo])
@inject
async def get_prediction_history(
        current_user_payload: Payload = Depends(get_current_user_payload),
        prediction_service: PredictionService = Depends(Provide[Container.prediction_service])
):
    prediction_history = prediction_service.get_prediction_history(current_user_payload.id)
    return prediction_history


@router.post("/make", response_model=PredictionBatchInfo)
@inject
async def make_predictions(
        prediction_request: PredictionRequest,
        current_user_payload: Payload = Depends(get_current_user_payload),
        prediction_service: PredictionService = Depends(Provide[Container.prediction_service]),
        predictor_service: PredictorService = Depends(Provide[Container.predictor_service]),
        billing_service: BillingService = Depends(Provide[Container.billing_service])
):
    if len(prediction_request.features) == 0:
        raise ValidationError("No features provided")
    model_cost_per_prediction = predictor_service.get_model_cost(prediction_request.model_name)
    total_cost = model_cost_per_prediction * len(prediction_request.features)
    if not billing_service.reserve_funds(current_user_payload.id, total_cost):
        raise PredictionError(detail="Insufficient funds for prediction batch.")

    try:
        batch_requests = [
            {'merchant_id': single_request.merchant_id, 'cluster_id': single_request.cluster_id}
            for single_request in prediction_request.features
        ]
        batch_result = prediction_service.make_batch_prediction(
            prediction_request.model_name,
            batch_requests
        )
        prediction_results = batch_result.get(timeout=30)

        predictions = []
        for result in prediction_results:
            predictions.append(PredictionInfo(
                features=PredictionFeatures(merchant_id=result['merchant_id'], cluster_id=result['cluster_id']),
                target=PredictionTarget(category_id=result['category_id'], category_label=result['category_label'])
            ))
    except ValueError as e:
        billing_service.cancel_reservation(current_user_payload.id, total_cost)
        raise PredictionError(detail=str(e))
    except Exception as e:
        billing_service.cancel_reservation(current_user_payload.id, total_cost)
        raise PredictionError(detail="An error occurred during prediction: " + str(e))
    try:
        transaction = billing_service.finalize_transaction(current_user_payload.id, total_cost)
        batch = prediction_service.save_batch_prediction(user_id=current_user_payload.id,
                                                         model_name=prediction_request.model_name,
                                                         transaction_id=transaction.id,
                                                         prediction_results=prediction_results)

        return PredictionBatchInfo(
            id=batch.id,
            model_name=prediction_request.model_name,
            predictions=predictions,
            timestamp=get_now(),
            cost=total_cost
        )
    except Exception as e:
        raise PredictionError(detail=str(e))
