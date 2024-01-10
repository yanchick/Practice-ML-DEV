from fastapi import APIRouter, Depends
from core.container import Container
from core.dependencies import get_current_active_user
from schema.model_schema import ModelInfo, Balance, Transaction
from services.billing_service import BillingService
from model.user import User
from repository.user_repository import UserRepository
from fastapi import HTTPException

router = APIRouter(prefix="/models", tags=["models"])

def get_user_repository():
    return Container.user_repository()

@router.get("/info", response_model=list[ModelInfo])
async def get_available_models(user_repository: UserRepository = Depends(get_user_repository)):
    models = user_repository.get_all_models()
    return [{"modelid": model.modelid, "description": model.description, "price": model.price} for model in models]


@router.get("/balance", response_model=Balance)
async def get_user_balance(current_user: User = Depends(get_current_active_user),
                           user_repository: UserRepository = Depends(get_user_repository)):
    user = user_repository.read_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"balance": user.balance}

@router.get("/history", response_model=list[Transaction])
async def get_user_transaction_history(current_user: User = Depends(get_current_active_user),
                                       user_repository: UserRepository = Depends(get_user_repository)):
    user = user_repository.read_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Assuming you have a method to get user transaction history in UserRepository
    transaction_history = user_repository.get_user_transaction_history(user.id)
    return transaction_history
