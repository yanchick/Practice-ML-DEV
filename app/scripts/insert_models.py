# scripts/insert_models.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, engine
from services import model_service
from database.models import Model
from database import get_db


def insert_models():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    if not model_service.get_models(db):
    # Run the script to insert models
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        models_data = [
            {"id": 1, "name": "random_forest_model", "cost": 20},
            {"id": 2, "name": "svm_model", "cost": 15},
            {"id": 3, "name": "xgboost_model", "cost": 10},
        ]

        for model_data in models_data:
            db_model = Model(**model_data)
            db.add(db_model)

        db.commit()

if __name__ == "__main__":
    insert_models()
