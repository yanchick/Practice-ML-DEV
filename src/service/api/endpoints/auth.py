
from typing import Annotated

from fastapi import APIRouter, Depends

from service.api.schemas import UserLogin, UserRegister, SignInResponse, User
from service.api.services.auth_service import AuthService, auth_service
from service.api.security import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(user_login_info: UserLogin, auth_service: Annotated[AuthService, Depends(auth_service)]) -> SignInResponse:
    """Sign in user. Returns token for user and saves it to cookie"""
    response = await auth_service.sing_in(user_login_info)
    return response


@router.post("/sign-up")
async def sign_up(user_register_info: UserRegister, auth_service: Annotated[AuthService, Depends(auth_service)]) -> SignInResponse:
    """Sign up user. Returns token for user and saves it to cookie"""
    response = await auth_service.sign_up(user_register_info)
    return response


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Test function to check dependancy injection"""
    return current_user
