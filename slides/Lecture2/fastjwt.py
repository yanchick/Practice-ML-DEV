from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import  HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# Ключ для подписи и проверки JWT токенов
SECRET_KEY = "mycoolsecretkey"


engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True)
    username = Column(String)
    password = Column(String)


class User(BaseModel):
    username: str
    password: str


# Функция для создания JWT токена
def create_token(username: str, password: str):
    # Здесь можно добавить логику проверки пароля
    # и других условий для авторизации пользователя
    user = session.query(DBUser).filter(DBUser.username == username).one()
    if user.password!= password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_payload = {"username": username}
    token = jwt.encode(token_payload, SECRET_KEY)
    return token


# Защищаемые роуты, требующие авторизации.
items = {"item1": "apple", "item2": "banana"}

# Защита маршрутов с использованием HTTPBearer
bearer = HTTPBearer()


@app.post("/login")
def login(user: User):
    # Проверяем правильность логина и пароля
    # В данном примере считаем авторизацию всегда успешной
    token = create_token(user.username, user.password)
    return {"access_token": token}


@app.get("/items")
def get_items(token: str = Depends(bearer)):
    try:
        # Проверяем JWT токен
        payload = jwt.decode(token.credentials, SECRET_KEY)
        username = payload.get("username")

        if username!= "admin":
            raise HTTPException(status_code=401, detail="Invalid token")
        # Авторизация успешна, возвращаем доступные элементы
        return items
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



