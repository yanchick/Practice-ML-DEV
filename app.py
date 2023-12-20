from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
import numpy as np
import logging
import pandas as pd  # Добавьте эту строку
from sqlalchemy.orm import Session
from database import PredictionRequestDB, PredictionResultDB
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы
    allow_headers=["*"],  # Разрешает все заголовки
)

# Загрузка модели
rf_model = load('random_forest_model.joblib')
le = load('label_encoder.joblib')
scaler = load('scaler.joblib')

# Модель запроса предсказания
class PredictionRequest(BaseModel):
    
    project: str
    case_id: str
    gender: str
    age_at_diagnosis: float
    primary_diagnosis: str
    race: str
    idh1: int
    tp53: int
    atrx: int
    pten: int
    egfr: int
    cic: int
    muc16: int
    pik3ca: int
    nf1: int
    pik3r1: int
    fubp1: int
    rb1: int
    notch1: int
    bcor: int
    csmd3: int
    smarca4: int
    grin2a: int
    idh2: int
    fat4: int
    pdgfra: int

# Модель ответа предсказания
class PredictionResponse(BaseModel):
    prediction: int  # Или float, в зависимости от того, какой тип данных возвращает ваша модель
    probability: float


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        input_data = transform_to_model_input(request)
        prediction = rf_model.predict(input_data)[0]
        probability = rf_model.predict_proba(input_data)[0][1]
        # Сохранение запроса в базу данных
        db_request = PredictionRequestDB(
            # Здесь передайте данные из запроса
            case_id=request.case_id,
            gender=request.gender,
            age_at_diagnosis=request.age_at_diagnosis,
            primary_diagnosis=request.primary_diagnosis,
            race=request.race,
            idh1=request.idh1,
            tp53=request.tp53,
            atrx=request.atrx,
            pten=request.pten,
            egfr=request.egfr,
            cic=request.cic,
            muc16=request.muc16,
            pik3ca=request.pik3ca,
            nf1=request.nf1,
            pik3r1=request.pik3r1,
            fubp1=request.fubp1,
            rb1=request.rb1,
            notch1=request.notch1,
            bcor=request.bcor,
            csmd3=request.csmd3,
            smarca4=request.smarca4,
            grin2a=request.grin2a,
            idh2=request.idh2,
            fat4=request.fat4,
            pdgfra=request.pdgfra
            )
        db_result = PredictionResultDB(
            request_id=db_request.id,  # ID запроса
            prediction=prediction,
            probability=probability
        )
        # Важно: Создаем сессию для каждой транзакции
        with SessionLocal() as session:
            session.add(db_request)
            session.commit()  # Сохраняем объект, чтобы он получил id

            db_result = PredictionResultDB(
                request_id=db_request.id,
                prediction=prediction,
                probability=probability
            )
            session.add(db_result)
            session.commit()


        return PredictionResponse(prediction=prediction, probability=probability)
    except Exception as e:
        logging.exception("Error during prediction")
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")
    

def transform_to_model_input(request: PredictionRequest) -> pd.DataFrame:
    # Создание DataFrame из входных данных запроса
    input_df = pd.DataFrame([request.dict()])

    # Преобразование названий столбцов в нижний регистр
    input_df.columns = [col.lower() for col in input_df.columns]

    # Применение LabelEncoder к категориальным столбцам
    for column in input_df.columns:
        if input_df[column].dtype == type(object):
            input_df[column] = safe_transform(le, input_df[column])

    # Масштабирование с использованием scaler
    scaled_data = scaler.transform(input_df)
    
    return scaled_data


def safe_transform(label_encoder, category):
    if isinstance(category, pd.Series):
        return category.apply(lambda x: label_encoder.transform([x])[0] if x in label_encoder.classes_ else -1)
    else:
        return label_encoder.transform([category])[0] if category in label_encoder.classes_ else -1
