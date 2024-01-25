from pathlib import Path
from datetime import datetime

import redis
import asyncio
import pandas as pd
from rq import Queue

from src.inference.model_wrapper import Catboost, RandomForest, SVC
from src.infrastructure.repository.predictions_repository import PredictionsRepository
from src.infrastructure.repository.user_repository import UserRepository

MODELS_PATH = Path("models")
MODELS_MAP = {
    'catboost': Catboost(),
    'random_forest': RandomForest(),
    'svc': SVC()
}

redis_conn = redis.Redis(host='localhost', port=6379)
q = Queue(connection=redis_conn)


async def predict(prediction_id, model_name, user_id, user_balance, *args, **kwargs):
    try:
        model = MODELS_MAP[model_name]

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
