from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.router.auth import get_current_user
from src.schemes.user_scemes import LoginResponse, SingupRequest, UserScheme

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> LoginResponse:
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    #
    # return {"access_token": user.username, "token_type": "bearer"}
    return LoginResponse(access_token="fake_token", token_type="bearer")


@router.get("/signup")
async def signup(user_info: SingupRequest) -> LoginResponse:
    # user_dict = fake_users_db.get(form_data.username)
    # if user_dict:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    #
    # return {"access_token": user.username, "token_type": "bearer"}
    return LoginResponse(access_token="fake_token", token_type="bearer")


@router.get("/me")
async def me(token: Annotated[str, Depends(get_current_user)]) -> UserScheme:
    # user_dict = fake_users_db.get(form_data.username)
    # if user_dict:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    #
    # return {"access_token": user.username, "token_type": "bearer"}
    return UserScheme(username="fake_username", balance=0.0)
