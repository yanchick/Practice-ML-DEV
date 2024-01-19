import sys
import json
import random

from pathlib import Path
from datetime import datetime
from time import sleep

import redis
import asyncio
import pandas as pd
from rq import Queue


sys.path.append(str(Path(__file__).resolve().parents[1]))
from inference.model_wrapper import Model, Lasso
from infrastructure.repository.predictions_repository import PredictionsRepository
from infrastructure.repository.user_repository import UserRepository

MODELS_PATH = Path("models")
MODELS_MAP = {
    'lasso': Lasso()
}

# Connect to Redis
redis_conn = redis.Redis(host='localhost', port=6379)
q = Queue(connection=redis_conn)

async def predict(prediction_id, model_name, model_cost, user_id, user_balance, **kwargs):
    try:
        model = MODELS_MAP[model_name]

        # Load the CSV file into a DataFrame
        if "file" in kwargs:
            data = pd.read_csv(kwargs["file"])
        else:
            return "No file provided"

        output = model.predict(data=data)

        update_data = {"prediction_date": datetime.now(),
                       "is_success": True,
                       "is_finished": True,
                       "output": output}
    
    except Exception as e:
        print(e)

        asyncio.create_task(UserRepository().update(data={"balance": user_balance}, id=user_id))

        update_data = {"prediction_date": datetime.now(),
                       "is_success": False,
                       "is_finished": True,
                       "error_info": str(e)}
    
    asyncio.create_task(PredictionsRepository().update(data=update_data, id=prediction_id))
