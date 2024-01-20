from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SignInRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address.")
    password: str = Field(..., description="User password.")


class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="New user email address.")
    password: str = Field(..., description="New user password.")
    name: str = Field(..., description="New user's full name.")


class Session(BaseModel):
    access_token: str = Field(..., description="JWT access token for authentication.")
    expiration: datetime = Field(..., description="Expiration time of the access token.")


class Payload(BaseModel):
    id: int = Field(..., description="Unique identifier of the user.")
    email: EmailStr = Field(..., description="Email address of the user.")
    name: str = Field(..., description="Full name of the user.")
    is_superuser: bool = Field(..., description="Flag indicating whether the user is a superuser.")
