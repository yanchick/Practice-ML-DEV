from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from celery import Celery
from datetime import datetime
import joblib
from typing import Optional

# Load the machine learning model
model = joblib.load("LR.pkl")

# Pydantic model for input validation
class PredictionInput(BaseModel):
    RIAGENDR: float
    PAQ605: float
    BMXBMI: float
    LBXGLU: float
    DIQ010: float
    LBXGLT: float
    LBXIN: float

# SQLAlchemy model for storing data in the database
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

# Initialize FastAPI app
app = FastAPI()

# Initialize SQLAlchemy database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Initialize Celery
celery = Celery(
    'tasks',
    broker='pyamqp://guest:guest@localhost//',
    backend='rpc://'
)

# Dependency to get the database session
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

        # Extract features from the database
        features = [
            prediction_data.RIAGENDR,
            prediction_data.PAQ605,
            prediction_data.BMXBMI,
            prediction_data.LBXGLU,
            prediction_data.DIQ010,
            prediction_data.LBXGLT,
            prediction_data.LBXIN
        ]

        # Perform prediction using the loaded machine learning model
        prediction_result = model.predict([features])[0]

        # Convert the prediction result to string 
        prediction_result = str(prediction_result)

        # Update the prediction result in the database
        prediction_data.prediction_result = prediction_result
        db.commit()

        return prediction_result
    finally:
        db.close()

# Endpoint to upload data for prediction
@app.post("/upload-data", response_model=None)
def upload_data(data: PredictionInput, db: Session = Depends(get_db)):
    # Store the data in the database
    db_data = PredictionData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    # Send the prediction task to Celery
    perform_prediction.apply_async(args=[db_data.id], countdown=5)  # Delayed execution after 5 seconds

    return db_data

# Endpoint to get prediction result
@app.get("/get-prediction-result/{prediction_id}")
def get_prediction_result(prediction_id: int, db: Session = Depends(get_db)):
    prediction_data = db.query(PredictionData).filter(PredictionData.id == prediction_id).first()

    if prediction_data:
        return {
            "prediction_result": prediction_data.prediction_result,
        }
    else:
        raise HTTPException(status_code=404, detail="Prediction not found")
