import pickle

from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime
from service.api.responses import HealthResponse
from pydantic import BaseModel
from service.log import app_logger

from sqlalchemy.orm import Session
from .database import SessionLocal, User, Job, Balance, engine, Base

Base.metadata.create_all(bind=engine)

router = APIRouter()
bearer = HTTPBearer()

# Secret key for JWT token
SECRET_KEY = "SECRET_TOKEN"
ALGORITHM = "HS256"

with open("service/api/models/model_lgbm.pkl", "rb") as file:
    lgbm_class = pickle.load(file)
    
with open("service/api/models/model_lr.pkl", "rb") as file:
    logreg_class = pickle.load(file)

with open("service/api/models/model_rf.pkl", "rb") as file:
    randforest_class = pickle.load(file)

with open("service/api/models/model_le_cluster.pkl", "rb") as file:
    labelenc_claster = pickle.load(file)

with open("service/api/models/model_le_product.pkl", "rb") as file:
    labelenc_product = pickle.load(file)
    

# Create an instance of CryptContext for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"])


# Define a Pydantic model for user registration data
class UserRegistration(BaseModel):
    username: str
    password: str


# Define a Pydantic model for input data
class PredictionInput(BaseModel):
    Product_Title: str
    Merchant_ID: int
    Cluster_ID: int
    Cluster_Label: str
    # Add more features as needed for your model
    
def get_model_names():
    return ["lgbm", "logreg", "randforest"]


# Define user data (for demonstration
USERS = [
    {"username": "admin", "password": "$2b$12$TpLt3BSS/7KaiU8zF1lXYODZD.mupmFsBkt1.YVb7jvv1UAv0rTXK"},
    
]


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to verify username and password
def verify_user(username, password):
    user = next((user for user in USERS if user["username"] == username), None)
    if user and pwd_context.verify(password, user["password"]):
        return user


# Function to create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def encode_feature(feature_value, label_encoder):
    feature_str = str(feature_value)
    if feature_str in label_encoder.classes_:
        encoded_feature = label_encoder.transform([feature_str])[0]
    else:
        encoded_feature = label_encoder.transform([''])[0]
    return encoded_feature


# OAuth2PasswordBearer is used to get the token from the request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    path="/health",
    tags=["Health"],
    responses={
        status.HTTP_200_OK: {"model": HealthResponse},
    },
)
async def health() -> str:
    return "I am alive"


@router.post("/register")
async def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user_data.password)
    try:
        db_user = User(username=user_data.username, password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Initialize user balance
        new_user_balance = Balance(current_balance=1000, user_id=db_user.id)
        db.add(new_user_balance)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already registered")


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Защищенный маршрут, который требует JWT авторизации
@router.get("/user/me")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    # Проверяем и декодируем токен
    payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token")

    # Fetch balance info
    balance = db.query(Balance).filter(Balance.user_id == user.id).first()
    balance_info = balance.current_balance if balance else 0
    
    jobs = db.query(Job).filter(Job.user_id == user.id).order_by(Job.start_time.desc()).limit(10).all()
    jobs_info = [{"model_name": job.model_name, "status": job.status, "cost": job.cost, "result": job.result} for job in jobs]
    
    return {"message": f"{username}", "balance": balance_info, "recent_jobs": jobs_info}


@router.post("/predict/{model_name}")
async def predict(input_data: PredictionInput, model_name: str, credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
        
        app_logger.info(f"Request for model: {model_name}")
        
        # Assuming get_model_names() is updated to check against available models in the database
        existing_models = get_model_names()

        encoded_product_title = encode_feature(input_data.Product_Title, labelenc_product)
        encoded_cluster_label = encode_feature(input_data.Cluster_Label, labelenc_claster)
        
        input_data = [[encoded_product_title, input_data.Merchant_ID, input_data.Cluster_ID, 
                encoded_cluster_label]]
        
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=403, detail="Invalid token")

        # Fetch user's balance
        balance = db.query(Balance).filter(Balance.user_id == user.id).first()

        # Perform the prediction
        prediction_status = "Started"
        
        if model_name == "lgbm":
            prediction_cost = 10
            if balance.current_balance >= prediction_cost:
                balance.current_balance -= prediction_cost
            else:
                raise HTTPException(status_code=400, detail="Insufficient balance")
            db.commit()
            result = lgbm_class.predict(input_data)
        elif model_name == "logreg":
            prediction_cost = 6
            if balance.current_balance >= prediction_cost:
                balance.current_balance -= prediction_cost
            else:
                raise HTTPException(status_code=400, detail="Insufficient balance")
        
            db.commit()
            result = logreg_class.predict(input_data)
        elif model_name == "randforest":
            prediction_cost = 8
            if balance.current_balance >= prediction_cost:
                balance.current_balance -= prediction_cost
            else:
                raise HTTPException(status_code=400, detail="Insufficient balance")
        
            db.commit()
            result = randforest_class.predict(input_data)
        else:
            raise HTTPException(status_code=404, detail="Model not found")
        
        prediction_status = "Completed"
        
        new_job = Job(
        status=prediction_status,
        model_name=model_name,
        start_time=datetime.utcnow(),
        cost=prediction_cost,
        result=str(result.tolist()),  # Convert result to string if needed
        user_id=user.id
    )
        db.add(new_job)
        db.commit()
        
        return {"pred": result.tolist(), "balance": balance.current_balance}

def add_views(app: FastAPI) -> None:
    app.include_router(router)