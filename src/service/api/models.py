from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, ForeignKey, Float
from service.api.db import Base


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    hash_password = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    balance = Column(Integer, default=500)


class DBPredictor(Base):
    __tablename__ = "predictor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False, unique=True)
    cost = Column(Integer)
    is_active = Column(Boolean, default=True)


class DBPredicton(Base):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    predicted_at = Column(DateTime(timezone=True))
    predictor_id = Column(Integer, ForeignKey("predictor.id"))
    input_data_type = Column(String(255))
    start_datatime = Column(DateTime, nullable=True, default=None)
    end_datatime = Column(DateTime, nullable=True, default=None)
    is_success = Column(Boolean)
    output_data = Column(String(255), nullable=False)


class DBData(Base):
    __tablename__ = "data"

    timestamp = Column(DateTime(timezone=True), primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    CO2CosIRValue = Column(Float)
    CO2MG811Value = Column(Float)
    MOX1 = Column(Float)
    MOX2 = Column(Float)
    MOX3 = Column(Float)
    MOX4 = Column(Float)
    COValue = Column(Float)
