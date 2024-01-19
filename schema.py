from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    Модель для хранения информации о пользователях ML-сервиса.
    Attributes:
        id (int): Уникальный идентификатор пользователя.
        email (str): Адрес электронной почты пользователя.
        password (str): Пароль пользователя.
        credits (int): Количество кредитов на счету пользователя.
        predictions (relationship): Отношение к предсказаниям, \
            связанным с пользователем.
        transactions (relationship): Отношение к транзакциям, \
            связанным с пользователем.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    credits = Column(Integer, default=50)
    predictions = relationship("Prediction", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    """
    Модель для хранения информации о транзакциях пользователя в ML-сервисе.
    Attributes:
        id (int): Уникальный идентификатор транзакции.
        user_id (int): Идентификатор пользователя,
        связанного с данной транзакцией.
        timestamp (DateTime): Временная метка транзакции.
        amount (int): Сумма транзакции.
        transaction_type (str): Тип транзакции \
            ('debit' - списание, 'credit' - зачисление).
        user (relationship): Отношение к пользователю, \
            связанному с данной транзакцией.
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'debit' or 'credit'
    user = relationship("User", back_populates="transactions")


class Model(Base):
    """
    Модель для хранения информации о различных ML-моделях.
    Attributes:
        id (int): Уникальный идентификатор модели.
        model (str): Название модели.
        description (str): Описание модели.
        cost_in_credits (int): Стоимость модели в кредитах.
    """

    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    model = Column(String, unique=True, nullable=False)
    description = Column(String)
    cost_in_credits = Column(Integer, nullable=False)


# Add models to our database
def add_default_models(session):
    """
    Добавляет три модели в базу данных.
    Args:
        session: Сеанс SQLAlchemy для взаимодействия с базой данных.
    """
    default_models = [
        Model(
            model="Catboost",
            description="Лучшее предсказание",
            cost_in_credits=30,
        ),
        Model(
            model="SVM",
            description="Самая быстрая работа",
            cost_in_credits=15,
        ),
        Model(
            model="Logistic regression",
            description="Линейная модель для классификации",
            cost_in_credits=5,
        ),
    ]

    session.add_all(default_models)
    session.commit()


class Prediction(Base):
    """
    Модель для хранения информации о предсказаниях в ML-сервисе.
    Attributes:
        id (int): Уникальный идентификатор предсказания.
        user_id (int): Идентификатор пользователя, связанного с предсказанием.
        result (str): Ссылка на файл предсказаний (путь или URL).
        user (relationship): Отношение к пользователю, 
            связанному с предсказанием.
    """

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    result = Column(String, nullable=False)
    user = relationship("User", back_populates="predictions")


# Далее, создаем базу данных и создаем таблицы
engine = create_engine("sqlite:///ml_service.db", echo=True)
Base.metadata.create_all(engine)

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Добавляем модели по умолчанию
add_default_models(session)

session.close()