from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pickle

app = FastAPI()

minmaxscaler = pickle.loads(
    joblib.load("ml_models/MinMaxScaler_pickle.joblib")
)
models = {
    0: pickle.loads(joblib.load("ml_models/LinearRegression_pickle.joblib")),
    1: pickle.loads(joblib.load("ml_models/DecisionTreeRegressor.joblib")),
    2: pickle.loads(joblib.load("ml_models/KNeighborsRegressor.joblib")),
}


class InputData(BaseModel):
    model: int
    age_group: int  # 0 for <65 or 1 for >=65
    RIAGENDR: float  # 0 for man or 1 for woman
    PAQ605: float  # how much days in a week man enjoys, sports and other 0 to 7
    BMXBMI: float  # Body mass index 14,5 to 70
    LBXGLU: float  # Уровень глюкозы после голодания 63 to 405
    DIQ010: float  # Степень диабета от 1 до 3
    LBXGLT: float  # Уровень гемоглобина от 40 до 604
    LBXIN: float  # Уровни инсулина в крови респондента от 1 до 102


@app.post("/predict")
def predict(data: InputData):
    try:
        if data.model == 0:
            result = models[0].predict(
                minmaxscaler.transform(
                    [
                        [
                            data.age_group,
                            data.RIAGENDR,
                            data.PAQ605,
                            data.BMXBMI,
                            data.LBXGLU,
                            data.DIQ010,
                            data.LBXGLT,
                            data.LBXIN,
                        ]
                    ]
                )
            )
        if data.model == 1:
            result = models[1].predict(
                minmaxscaler.transform(
                    [
                        [
                            data.age_group,
                            data.RIAGENDR,
                            data.PAQ605,
                            data.BMXBMI,
                            data.LBXGLU,
                            data.DIQ010,
                            data.LBXGLT,
                            data.LBXIN,
                        ]
                    ]
                )
            )
        if data.model == 2:
            result = models[2].predict(
                minmaxscaler.transform(
                    [
                        [
                            data.age_group,
                            data.RIAGENDR,
                            data.PAQ605,
                            data.BMXBMI,
                            data.LBXGLU,
                            data.DIQ010,
                            data.LBXGLT,
                            data.LBXIN,
                        ]
                    ]
                )
            )
        return {
            "prediction": result.tolist(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}"
        )
