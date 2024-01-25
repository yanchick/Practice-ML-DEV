from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, ForeignKey, Float, JSON


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer, default=1000)


class Models(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cost = Column(Integer)


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    model_id = Column(Integer)
    prediction_date = Column(DateTime(timezone=True), default=func.now())
    is_success = Column(Boolean)
    is_finished = Column(Boolean)
    error_info = Column(String)
    output = Column(JSON, nullable=True)
