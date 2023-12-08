from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Настройки приложения
DATABASE_URL = "sqlite:///./test.db"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Создаем экземпляр FastAPI
app = FastAPI()

# Создаем модель пользователя
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Создаем базу данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем хешер паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создаем токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Определение модели для создания нового пользователя
class UserCreate(BaseModel):
    username: str
    password: str

# Определение JWT токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Функция для создания JWT токена
def create_jwt_token(data: dict):
    to_encode = jsonable_encoder(data)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Роут для создания нового пользователя
@app.post("/users/", response_model=Token)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_jwt_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Функция для получения базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для получения текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# Роут для получения информации о текущем пользователе
@app.get("/users/me/", response_model=str)
def read_users_me(current_user: str = Depends(get_current_user)):
    return current_user