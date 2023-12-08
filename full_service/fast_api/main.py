from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from infrastructure.handlers.main import Inference_handler


from infrastructure.database.database_functions import (
    get_user_by_username,
    get_bill_by_user_id,
    get_predict_rows_by_user,
    update_bill,
    create_user,
    delete_user,
    update_user_fields,
    create_bill,
    add_predict_row,
    authenticate_user,
)

from jwt_work.main import JWT_worker


class InputData(BaseModel):
    model: int
    age_group: int
    RIAGENDR: float
    PAQ605: float
    BMXBMI: float
    LBXGLU: float
    DIQ010: float
    LBXGLT: float
    LBXIN: float


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
    # try:
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


# except:
#     raise HTTPException(status_code=409, detail="User if registered")


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


# Отправка данных для обработки моделью
@app.post("/send_data")
def send_data_for_processing(
    data: InputData, current_user: str = Depends(JWT_worker.get_current_user)
):
    user = get_user_by_username(current_user)
    if user:
        result = Inference_handler.predict(data)
        add_predict_row(
            user.id,
            data.age_group,
            data.gender,
            data.sport_days,
            data.bmi,
            data.glucose,
            data.diabetes_degree,
            data.hemoglobin,
            data.insulin,
            result,
        )
        return {"message": "Data processed successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/bill")
def get_user_bill(current_user: str = Depends(JWT_worker.get_current_user)):
    user = get_user_by_username(current_user)
    if user:
        bill = get_bill_by_user_id(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "bill": bill.money if bill > 0 else 0.0,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/predict_rows")
def get_user_predict_rows(
    current_user: str = Depends(JWT_worker.get_current_user),
):
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
