from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./sqlite.db"
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    model_name = Column(String)
    start_time = Column(DateTime)
    cost = Column(Numeric(19, 0))
    result = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Balance(Base):
    __tablename__ = "balances"
    id = Column(Integer, primary_key=True, index=True)
    current_balance = Column(Numeric(19, 0))
    user_id = Column(Integer, ForeignKey("users.id"))

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Base.metadata.drop_all(bind=engine) 