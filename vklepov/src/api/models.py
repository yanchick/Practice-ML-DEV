"""Database models for malware detector app."""

from fastapi import Depends
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import mapped_column, Session, Mapped
from .database import Base, get_async_session
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class BalanceDebit(Base):
    """User account debits."""

    __tablename__ = "debits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Integer)


class Job(Base):
    """Computation executed in the service."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    status = Column(Integer)
    cost = Column(Integer)
    # ISO8601
    created_at = Column(Text)
    result = Column(Text)


async def get_user_db(session: Session = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
