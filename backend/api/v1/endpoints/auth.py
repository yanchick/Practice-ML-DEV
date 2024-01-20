from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from backend.core.container import Container
from backend.schema.auth_schema import SignInRequest, SignUpRequest
from backend.schema.user_schema import BaseUser
from backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=BaseUser)
@inject
async def sign_in(user_info: SignInRequest, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_in(user_info)


@router.post("/sign-up", response_model=BaseUser)
@inject
async def sign_up(user_info: SignUpRequest, service: AuthService = Depends(Provide[Container.auth_service])):
    return service.sign_up(user_info)
