from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_token = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    password_hash = Column(String)

    billing = relationship("Billing", back_populates="user")
    predictions = relationship("Prediction", back_populates="user")
    billing_history = relationship("BillingHistory", back_populates="user")


class Billing(Base):
    __tablename__ = 'billing'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    points = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="billing")


class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(String)
    product_title = Column(String)
    merchant_id = Column(String)
    cluster_id = Column(String)
    cluster_label = Column(String)
    category_id = Column(String)
    category_label = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="predictions")


class BillingHistory(Base):
    __tablename__ = 'billing_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    points_changed = Column(Integer)
    reason = Column(String)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="billing_history")


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    cost = Column(Float)

    predictions = relationship("Prediction", back_populates="model")
