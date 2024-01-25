from typing import Annotated

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject

from src.api.schemas.auth_schema import UserLogin, UserRegister, UserLoginResponse, User, Balance
from src.infrastructure.services.auth_service import AuthService, get_auth_service
from src.infrastructure.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginResponse)
@inject
async def login(user_info: UserLogin,
                service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.login(user_info)
    return response


@router.post("/register", response_model=UserLoginResponse)
@inject
async def register(user_info: UserRegister,
                   service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.register(user_info)
    return response


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/balance", response_model=Balance)
async def get_balance(service: Annotated[AuthService, Depends(get_auth_service)],
                      current_user: User = Depends(get_current_user)):
    response = await service.get_balance(current_user)
    return response
