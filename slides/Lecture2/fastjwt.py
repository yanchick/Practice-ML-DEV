from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import JWTBearer, HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI()

# Ключ для подписи и проверки JWT токенов
SECRET_KEY = "mysecretkey"


class User(BaseModel):
    username: str
    password: str


# Функция для создания JWT токена
def create_token(username: str, password: str):
    # Здесь можно добавить логику проверки пароля
    # и других условий для авторизации пользователя

    token_payload = {"username": username}
    token = jwt.encode(token_payload, SECRET_KEY)
    return token


# Защищаемые роуты, требующие авторизации.
items = {"item1": "apple", "item2": "banana"}

# Защита маршрутов с использованием JWTBearer
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

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Авторизация успешна, возвращаем доступные элементы
        return items
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



