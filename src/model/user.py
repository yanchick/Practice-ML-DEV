from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, index=True)
    password = Column(String)
    user_token = Column(String, unique=True)
    balance = Column(Integer, default=0)
    name = Column(String, default=None, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    chosen_model_id = Column(Integer, default=0, nullable=True)
    temp_uploaded_data = Column(JSON, nullable=True) # Assuming temp_uploaded_data is a JSON string

# Assuming you have a separate file for database initialization
# For example, in core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "sqlite:///./temp.db"  # Use your actual database URI

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use this SessionLocal to interact with the database in your code









