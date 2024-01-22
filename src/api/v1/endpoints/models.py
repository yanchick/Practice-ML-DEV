from fastapi import APIRouter, Depends
from typing import Annotated
from core.container import Container
from core.dependencies import get_current_active_user
from schema.model_schema import ModelInfo, Balance, Transaction
from services.billing_service import BillingService
from model.user import User
from repository.user_repository import UserRepository
from repository.model_repository import ModelRepository
from fastapi import HTTPException

router = APIRouter(prefix="/models", tags=["models"])


from sqlalchemy.ext.asyncio import AsyncSession


#Session = Annotated[AsyncSession, Depends(get_session)]

def get_user_repository():
    return Container.user_repository()

def get_model_repository():
    return Container.model_repository()
#def get_user_repository():
  #  return Container.model_repository()


@router.get("/info", response_model=list[ModelInfo])
async def get_available_models(model_repository: ModelRepository = Depends(get_model_repository)):
    models = model_repository.get_all_models()
    return [{"modelid": model.modelid, "description": model.description, "price": model.price} for model in models]

#@router.get("/info")
#async def get_available_models(session: Session) -> list[ModelInfo]:
 #   models = await ModelRepository.get_all_models(session)
  #  if models:
   #     return list[ModelInfo](
    #        [{"modelid": model.modelid, "description": model.description, "price": model.price} for model in models])
    #else:
     #   return ModelInfo(models=[])


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
