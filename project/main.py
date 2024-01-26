from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from celery import Celery
from datetime import datetime, timedelta
import joblib
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext


model = joblib.load("LR.pkl")


class PredictionInput(BaseModel):
    RIAGENDR: float
    PAQ605: float
    BMXBMI: float
    LBXGLU: float
    DIQ010: float
    LBXGLT: float
    LBXIN: float


class User(BaseModel):
    username: str
    # email: str
    hashed_password: str


Base = declarative_base()

class PredictionData(Base):
    __tablename__ = "prediction_data"
    id = Column(Integer, primary_key=True, index=True)
    RIAGENDR = Column(Float)
    PAQ605 = Column(Float)
    BMXBMI = Column(Float)
    LBXGLU = Column(Float)
    DIQ010 = Column(Float)
    LBXGLT = Column(Float)
    LBXIN = Column(Float)
    prediction_result = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


app = FastAPI()


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)


celery = Celery(
    'tasks',
    broker='pyamqp://guest:guest@localhost//',
    backend='rpc://'
)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@celery.task
def perform_prediction(prediction_id: int):
    db = Session(engine)
    try:
        prediction_data = db.query(PredictionData).filter(PredictionData.id == prediction_id).first()
        features = [
            prediction_data.RIAGENDR,
            prediction_data.PAQ605,
            prediction_data.BMXBMI,
            prediction_data.LBXGLU,
            prediction_data.DIQ010,
            prediction_data.LBXGLT,
            prediction_data.LBXIN
        ]


        prediction_result = model.predict([features])[0]
        prediction_result = str(prediction_result)
        prediction_data.prediction_result = prediction_result
        db.commit()

        return prediction_result
    finally:
        db.close()

SECRET_KEY = "sc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@app.post("/sign-up")
def sign_up(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}


@app.post("/sign-in")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/upload-data", response_model=None)
def upload_data(data: PredictionInput, token: str = Depends(get_current_user), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_data = PredictionData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    perform_prediction.apply_async(args=[db_data.id], countdown=5)
    return db_data


@app.get("/get-prediction-result/{prediction_id}")
def get_prediction_result(prediction_id: int, token: str = Depends(get_current_user), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prediction_data = db.query(PredictionData).filter(PredictionData.id == prediction_id).first()
    if prediction_data:
        return {
            "prediction_result": prediction_data.prediction_result,
        }
    else:
        raise HTTPException(status_code=404, detail="Prediction not found")
