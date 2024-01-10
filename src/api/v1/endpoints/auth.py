import sys
from typing import Annotated
from pathlib import Path

from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

sys.path.append(str(Path(__file__).resolve().parents[3]))
from api.v1.schemas.auth_schema import UserLogin, UserRegister, UserLoginResponse, User
from infrastructure.services.auth_service import AuthService, get_auth_service
from infrastructure.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginResponse)
@inject
async def login(user_info: UserLogin, service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.login(user_info)
    return response

@router.post("/register", response_model=UserLoginResponse)
@inject
async def register(user_info: UserRegister, service: Annotated[AuthService, Depends(get_auth_service)]):
    response = await service.register(user_info)
    return response


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
