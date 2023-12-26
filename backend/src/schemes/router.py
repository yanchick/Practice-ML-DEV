from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session_manager import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")
TokenDepends = Annotated[str, Depends(oauth2_scheme)]


Session = Annotated[AsyncSession, Depends(get_session)]
AuthFormData = Annotated[OAuth2PasswordRequestForm, Depends()]
