from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.database import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/user/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    # user = fake_decode_token(token)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return user
    ...
