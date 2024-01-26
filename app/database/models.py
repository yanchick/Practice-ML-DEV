from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    credits = Column(Integer, index=True, default=999)
    
    interactions = relationship("Action", back_populates="user")


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Integer, index=True)
    
    interactions = relationship("Action", back_populates="model")
    
    
class Action(Base):
    __tablename__ = "actions"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(String, index=False)
    
    user = relationship("User", back_populates="interactions")
    model = relationship("Model", back_populates="interactions")
    
    # __table_args__ = (
    #     PrimaryKeyConstraint('user_id', 'model_id', name='actions_pk'),
    # )

class UserModel(Base):
    __tablename__ = "user_models"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), primary_key=True)
