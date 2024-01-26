from datetime import datetime
from typing import ClassVar
#from typing import List, Optional
from sqlmodel import Field, Text
from  model.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#Base = declarative_base()


class User(BaseModel):
    email: str = Text()
    password: str = Text()
    user_token: str = Field(unique=True)
    balance: int = Field(default=500)
    name: ClassVar[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    #last_sign_in = Column(DateTime)
    #transactions = relationship('Transaction', back_populates='user')
    #predictions = relationship('Prediction', back_populates='user')

#class User(Base):
 #   __tablename__ = 'users'
  #  user_id = Column(Integer, primary_key=True)
   # login = Column(String, unique=True, nullable=False)
   # email = Column(String, unique=True, nullable=False)

    #balance = Column(Float, default=0.0)
    #transactions = relationship('Transaction', back_populates='user')
    #predictions = relationship('Prediction', back_populates='user')
#class User(Base):
 #   __tablename__ = "users"
  #  id = Column(Integer, primary_key=True, index=True, nullable=False)
   # email = Column(String, index=True)
    #password = Column(String)
    #user_token = Column(String, unique=True)
    #balance = Column(Integer, default=0)
    #name = Column(String, default=None, nullable=True)
    #is_active = Column(Boolean, default=True)
    #is_superuser = Column(Boolean, default=False)
    #created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    #updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    #chosen_model_id = Column(Integer, default=0, nullable=True)
    #temp_uploaded_data = Column(JSON, nullable=True) # Assuming temp_uploaded_data is a JSON string

# Assuming you have a separate file for database initialization
# For example, in core/database.py
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker

#DATABASE_URI = "sqlite:///./temp.db"  # Use your actual database URI

#engine = create_engine(DATABASE_URI)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use this SessionLocal to interact with the database in your code









