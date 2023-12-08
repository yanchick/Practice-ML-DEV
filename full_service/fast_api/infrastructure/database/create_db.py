from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship
from .configs import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Bill(Base):
    __tablename__ = "Bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    money = Column(Float, nullable=False)

    user = relationship("User", back_populates="bills")


class PredictRow(Base):
    __tablename__ = "Predict_row"

    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    age_group = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    sport_days = Column(Integer, nullable=False)
    bmi = Column(Float, nullable=False)
    glucose = Column(Float, nullable=False)
    diabetes_degree = Column(Float, nullable=False)
    hemoglobin = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

    user = relationship("User", back_populates="predictions")


User.bills = relationship(
    "Bill",
    order_by=Bill.id,
    back_populates="user",
)
User.predictions = relationship(
    "PredictRow",
    order_by=User.id,
    back_populates="user",
)
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)
