from .configs import DATABASE_URL
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    select,
    delete,
    update,
)
import bcrypt
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session, sessionmaker

from .create_db import Bill, User, PredictRow


def session_commit(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def get_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(username, session=get_session()):
    return session.query(User).filter_by(username=username).first()


def get_bill_by_user_id(user_id, session=get_session()):
    return session.query(Bill).filter_by(User_id=user_id).first()


def get_predict_rows_by_user(user_id, session=get_session()):
    return session.query(PredictRow).filter_by(User_id=user_id).all()


def update_bill(bill_id, new_money_value, session=get_session()):
    bill = session.query(Bill).get(bill_id)
    if bill:
        bill.money = new_money_value
        session_commit(session)


def create_user(
    username,
    password,
    name,
    surname,
    session=get_session(),
):
    new_user = User(
        username=username,
        hashed_password=hash_password(password),
        name=name,
        surname=surname,
    )

    session.add(new_user)
    session_commit(session)
    new_bill = create_bill(user_id=new_user.id, money=1000)
    session.add(new_bill)
    session_commit(session)
    return new_user


def create_bill(
    user_id,
    money,
    session=get_session(),
):
    new_bill = Bill(
        User_id=user_id,
        money=money,
    )

    return new_bill


def delete_user(
    user_id,
    session=get_session(),
):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session_commit(session)


def update_user_fields(
    user_id,
    new_username=None,
    new_hashed_password=None,
    new_name=None,
    new_surname=None,
    session=get_session(),
):
    user = session.query(User).get(user_id)
    if user:
        if new_username:
            user.username = new_username
        if new_hashed_password:
            user.hashed_password = new_hashed_password
        if new_name:
            user.name = new_name
        if new_surname:
            user.surname = new_surname
        session_commit(session)


def add_predict_row(
    user_id,
    age_group,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
    result,
    session=get_session(),
):
    new_predict_row = PredictRow(
        User_id=user_id,
        age_group=age_group,
        gender=gender,
        sport_days=sport_days,
        bmi=bmi,
        glucose=glucose,
        diabetes_degree=diabetes_degree,
        hemoglobin=hemoglobin,
        insulin=insulin,
        result=result,
    )
    session.add(new_predict_row)
    session_commit(session)
    return new_predict_row


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def authenticate_user(
    username: str,
    password: str,
    session=get_session(),
):
    user = session.query(User).filter(User.username == username).first()

    if user and verify_password(password, user.hashed_password):
        return user

    return None
