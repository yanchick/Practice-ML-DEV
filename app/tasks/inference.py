# tasks/inference.py

from celery import Celery
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import joblib
import pandas as pd
from services import model_service
import json
from services.model_service import write_action
from database import get_db
import requests

# db_session = get_db()
BACKEND_URL = os.getenv('BACKEND_URL')
rf_model = joblib.load('/app/tasks/models/new_base_rf.joblib')
# svm_model = joblib.load('/app/tasks/models/svm_model.joblib')
# xgboost_model = joblib.load('/app/tasks/models/xgboost_model.joblib')


celery = Celery('tasks', broker=os.getenv('BROKER_URL'))

@celery.task
def perform_inference(user_id: str, model_id: int, input_data: str):
    print(input_data)
    # input_data = json.loads(input_data)
    # print(f"SECOND STEP \b {input_data}")
    input_data = pre_processing(input_data)

    if 1 == 1:
        res = rf_model.predict(input_data)
    # elif model_id == 2:
    #     res = svm_model.predict(input_data)
    # else:
    #     res = xgboost_model.predict(input_data)
    res = pd.DataFrame(res)
    res = res.to_json(orient='records') 
    # write_action(db_session, user_id, model_id, res.to_json(orient='records'))
    response = requests.post(f"{BACKEND_URL}/model/action",
                    params={
                    "user_id": f"{user_id}",
                    "model_id": f"{1}",
                    "result": f"{res}"
                    },) 
    return res
    
def pre_processing(data):
    df = pd.read_json(data)

    df = df.rename(columns={' Merchant ID':'Merchant ID', 
                        ' Cluster ID':'Cluster ID',
                        ' Cluster Label':'Cluster Label',
                        ' Category ID':'Category ID',
                        ' Category Label':'Category Label'
                       })

    # Word count feature
    df['word_count'] = df['Product Title'].apply(lambda x: len(str(x).split()))

    # Character count feature
    df['char_count'] = df['Product Title'].apply(lambda x: len(str(x)))

    # Average word length feature
    df['avg_word_length'] = df['char_count'] / df['word_count']

    columns_to_drop = ['Product ID', 'Merchant ID', 'Cluster ID', 'Category ID']
    df_cleared = df.drop(columns=columns_to_drop, axis=1)
    X = df_cleared.drop('Category Label', axis=1)

    return X
