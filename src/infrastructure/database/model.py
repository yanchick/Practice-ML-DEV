from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float


class Base(DeclarativeBase): pass


class Users(Base):
    __tablename__ = "users"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password_salt = Column(String)
    balance = Column(Integer, default=500)

    def __repr__(self):
        """
        Get set: {name, email, password (salt)}
        :returns: Set
        """
        return self.id, self.name, self.email, self.password_salt, self.balance


class Bills(Base):
    __tablename__ = "bills"
  
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bill_type = Column(String)
    coins_diff = Column(Integer)
    description = Column(String)
    time = Column(String)

    def __repr__(self):
        """
        Get set: {id, user_id, bill_type, coins_diff, description, time}
        :returns: Set
        """
        return self.id, self.user_id, self.bill_type, self.coins_diff, self.description, self.time


class Models(Base):
    __tablename__ = "models"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    model_type = Column(String)
    prediction_cost = Column(Integer)

    def __repr__(self):
        """
        Get set: {id, name, model_type, prediction_cost}
        :returns: Set
        """
        return self.id, self.name, self.model_type, self.prediction_cost


class Predictions(Base):
    __tablename__ = "predictions"
  
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    model_id = Column(Integer)
    input_path = Column(String)
    status = Column(String)
    result = Column(Float)

    def __repr__(self):
        """
        Get set: {id, user_id, model_id, input_path, status, result}
        :returns: Set
        """
        return self.id, self.user_id, self.model_id, self.input_path, self.status, self.result
