from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from backend.core.container import Container
from backend.core.dependencies import get_current_user_payload
from backend.core.exceptions import ValidationError
from backend.schema.auth_schema import Payload
from backend.schema.billing_schema import DepositRequest, TransactionInfo
from backend.services.billing_service import BillingService

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


@router.get("/balance", response_model=int)
@inject
async def get_balance(
        current_user_payload: Payload = Depends(get_current_user_payload),
        billing_service: BillingService = Depends(Provide[Container.billing_service])
):
    balance = billing_service.get_balance(current_user_payload.id)
    return balance


@router.get("/history", response_model=List[TransactionInfo])
@inject
async def get_transaction_history(
        current_user_payload: Payload = Depends(get_current_user_payload),
        billing_service: BillingService = Depends(Provide[Container.billing_service])
):
    transactions = billing_service.get_transaction_history(current_user_payload.id)
    return transactions


@router.post("/deposit", response_model=TransactionInfo)
@inject
async def deposit_funds(
        deposit_request: DepositRequest,
        current_user_payload: Payload = Depends(get_current_user_payload),
        billing_service: BillingService = Depends(Provide[Container.billing_service])
):
    if deposit_request.amount <= 0:
        raise ValidationError(detail="Deposit amount must be positive.")
    transaction = billing_service.deposit(current_user_payload.id, deposit_request.amount)
    return transaction
