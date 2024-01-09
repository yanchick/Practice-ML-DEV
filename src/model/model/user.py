from sqlmodel import SQLModel, Field, Text
from sqlalchemy import ARRAY
from datetime import datetime
from typing import List, Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True, nullable=False)
    email: str = Field(index=True)
    password: str = Field()
    user_token: str = Field(unique=True)
    balance: int = Field(default=500)
    name: str = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)


