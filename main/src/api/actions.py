from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Header

from schemas import User, Login, Billing, ActionsHistory
from auth import create_jwt_token, get_current_user


app = FastAPI()  # TODO: move to app.py
users_db = {}  # TODO: add db
tokens_db = {}  # TODO: add db


@app.post("/auth/register")
def register_user(user: User):
    '''
    Registration endpoint

    :returns: None
    '''
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = user.dict()
    return {"message": "User registered successfully"}

# Login endpoint
@app.post("/auth/login")
def login_user(login_details: Login):
    '''
    Login endpoint

    :returns: None
    '''
    user = users_db.get(login_details.email)
    if user and user["password"] == login_details.password:
        token_data = {"sub": login_details.email}
        token = create_jwt_token(token_data)
        tokens_db[token] = login_details.email
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/predict")
def send_data_for_prediction(
    file: UploadFile,
    model_name: str,
    authorization: str = Header(),
    current_user: str = Depends(get_current_user),
):
    '''
    Prediction request endpoint
    '''
    return {"message": "Input sent successfully"}

@app.get("/predict")
def get_prediction_results(authorization: str = Header(...)):
    '''
    Predictions result endpoint
    '''
    current_user = get_current_user(authorization)
    # implementation to get prediction results goes here
    return {"prediction": 0.75}

# Billing endpoints (mock implementation)
@app.get("/billing/balance")
def check_user_balance(authorization: str = Header(...), current_user: str = Depends(get_current_user)):
    '''
    Check coins balance endpoint
    '''
    # implementation to check user balance goes here
    return {"balance": 100}

@app.post("/billing/balance")
def add_spend_coins(billing_details: Billing, authorization: str = Header(...), current_user: str = Depends(get_current_user)):
    '''
    Add/spend coins endpoint
    '''
    # implementation to add/spend coins goes here
    return {"message": "Balance updated successfully"}

@app.get("/history")
def view_actions_history(authorization: str = Header(...), current_user: str = Depends(get_current_user)):
    '''
    Actions history endpoint
    '''
    # implementation to view user actions history goes here
    history = [
        {"ID": 1, "Type": "Add", "CoinsDiff": 10, "Description": "Added coins", "Time": "2023-01-01T12:00:00"},
        {"ID": 2, "Type": "Spend", "CoinsDiff": -5, "Description": "Spent coins on prediction", "Time": "2023-01-02T14:30:00"},
    ]
    return history
