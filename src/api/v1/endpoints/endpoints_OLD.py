import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header

from schemas.auth_schema import UserRegister, UserLogin, UserLoginResponse

sys.path.append(str(Path(__file__).resolve().parents[2]))
from infrastructure.core.security import create_jwt_token, decode_jwt_token, oauth2_scheme
from infrastructure.core.exceptions import AuthError
from infrastructure.services.auth_service import AuthService, get_auth_service
from api.v1.schemas import UserRegister, UserLogin, Billing, Prediction, ActionsHistory


router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = get_auth_service()


@router.post("/auth/register")
def register_user(reg_details: UserRegister, auth_service: Annotated[AuthService, Depends(auth_service)]) -> UserLoginResponse:
    '''
    Registration endpoint

    :returns: None
    '''
    return {"message": "User registered successfully"}

# Login endpoint
@router.post("/auth/login")
def login_user(login_details: UserLogin):
    '''
    Login endpoint

    :returns: None
    '''
    auth_service.sign_in(user_login_info)
    raise AuthError(detail="Invalid credentials")


@router.post("/predict")
def send_data_for_prediction(file: UploadFile, model_name: str):
    '''
    Prediction request endpoint
    '''
    return Prediction(2.5)

@router.get("/predict")
def get_prediction_results(model_name: str):
    '''
    Predictions result endpoint
    '''
    return Prediction(1.2)

# Billing endpoints (mock implementation)
@router.get("/billing/balance")
def check_user_balance():
    '''
    Check coins balance endpoint
    '''
    return Billing(500)

@router.post("/billing/balance")
def add_spend_coins(coins_diff: int):
    '''
    Add/spend coins endpoint
    '''
    return Billing(550)

@router.get("/history")
def view_actions_history():
    '''
    Actions history endpoint
    '''

    history = [
        {"ID": 1, "Type": "Add", "CoinsDiff": 10, "Description": "Added coins", "Time": "2023-01-01T12:00:00"},
        {"ID": 2, "Type": "Spend", "CoinsDiff": -5, "Description": "Spent coins on prediction", "Time": "2023-01-02T14:30:00"},
    ]
    return ActionsHistory(**history[0])
