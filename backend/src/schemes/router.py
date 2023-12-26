from enum import Enum
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session_manager import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")
TokenDepends = Annotated[str, Depends(oauth2_scheme)]

Session = Annotated[AsyncSession, Depends(get_session)]
AuthFormData = Annotated[OAuth2PasswordRequestForm, Depends()]


class OpenAPIResponses(dict, Enum):
    HTTP_401_UNAUTHORIZED = {
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials",
                        "headers": {"WWW-Authenticate": "Bearer"},
                        "status_code": 401,
                    }
                }
            },
        }
    }

    HTTP_400_BAD_REQUEST = {
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Username already registered",
                        "status_code": 400,
                    }
                }
            },
        }
    }

    HTTP_422_UNPROCESSABLE_ENTITY = {
        422: {
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "username"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ],
                        "status_code": 422,
                    }
                }
            },
        }
    }
