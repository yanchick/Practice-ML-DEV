from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Any
from configs.main import model_to_money

from infrastructure.handlers.main import Inference_handler

from infrastructure.database.database_functions import (
    get_user_by_username,
    get_bill_by_user_id,
    get_predict_rows_by_user,
    update_bill,
    create_user,
    add_predict_row,
    authenticate_user,
    get_predict_rows_by_user_and_data,
)

from jwt_work.main import JWT_worker


class InputData(BaseModel):
    model: int
    age_group: Any
    RIAGENDR: Any
    PAQ605: Any
    BMXBMI: Any
    LBXGLU: Any
    DIQ010: Any
    LBXGLT: Any
    LBXIN: Any
    token: str


class PersonalData(BaseModel):
    username: str
    password: str
    name: str
    surname: str


app = FastAPI()

main_handler = Inference_handler()
jwt_worker = JWT_worker()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register")
def register_user(pd: PersonalData):
    user = create_user(
        username=pd.username,
        password=pd.password,
        name=pd.name,
        surname=pd.surname,
    )

    return {
        "user_id": user.id,
        "username": user.username,
        "name": user.name,
        "surname": user.surname,
    }


@app.post("/add_row")
async def add_row(request: Request):
    json_body = await request.json()
    add_predict_row(
        user_id=json_body["user_id"],
        model=json_body["model"],
        age_group=json_body["age_group"],
        gender=json_body["gender"],
        sport_days=json_body["sport_days"],
        bmi=json_body["bmi"],
        glucose=json_body["glucose"],
        diabetes_degree=json_body["diabetes_degree"],
        hemoglobin=json_body["hemoglobin"],
        insulin=json_body["insulin"],
        result=json_body["result"],
    )


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = jwt_worker.create_access_token(
        data={
            "username": user.username,
            "password": user.hashed_password,
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/send_data")
async def send_data_for_processing(data: InputData):
    current_user = jwt_worker.get_current_user(data.token)
    user = get_user_by_username(current_user)
    type_of_res = "None"
    if user:
        bill = get_bill_by_user_id(user.id)
        cost = model_to_money[int(data.model)]
        checked_data = main_handler._check_data(
            data.model,
            data.age_group,
            data.RIAGENDR,
            data.PAQ605,
            data.BMXBMI,
            data.LBXGLU,
            data.DIQ010,
            data.LBXGLT,
            data.LBXIN,
        )
        old_rows = get_predict_rows_by_user_and_data(
            user.id,
            checked_data[0],
            checked_data[1],
            checked_data[2],
            checked_data[3],
            checked_data[4],
            checked_data[5],
            checked_data[6],
            checked_data[7],
            checked_data[8],
        )
        if len(old_rows) > 0:
            result = old_rows[0].result
            type_of_res = "History"
        else:
            type_of_res = "Predict"
            if (bill.money - cost) >= 0:
                result = main_handler.predict(
                    user.id,
                    data.model,
                    data.age_group,
                    data.RIAGENDR,
                    data.PAQ605,
                    data.BMXBMI,
                    data.LBXGLU,
                    data.DIQ010,
                    data.LBXGLT,
                    data.LBXIN,
                )
            else:
                return {"message": "Not enough units in account"}
        if result is not None:
            if type_of_res == "Predict":
                if update_bill(bill.id, bill.money - cost):
                    return {"message": "Data processed successfully"}
                else:
                    raise HTTPException(
                        status_code=404, detail="User not found"
                    )
            else:
                return {"message": "Data founded in history"}
        else:
            return {"message": "Data processing failed"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/bill")
def get_user_bill(request: Request):
    headers = request.headers
    current_user = jwt_worker.get_current_user(headers["Authorization"])
    user = get_user_by_username(current_user)
    if user:
        bill = get_bill_by_user_id(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "bill": bill.money if bill.money > 0 else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/predict_rows")
def get_user_predict_rows(request: Request):
    headers = request.headers
    current_user = jwt_worker.get_current_user(headers["Authorization"])
    user = get_user_by_username(current_user)
    if user:
        predict_rows = get_predict_rows_by_user(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "predict_rows": predict_rows,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
