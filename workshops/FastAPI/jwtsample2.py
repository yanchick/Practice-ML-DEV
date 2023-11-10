from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jwt import PyJWTError, decode, encode

app = FastAPI()

# Необходимо сгенерировать секретный ключ для JWT
SECRET_KEY = "your-secret-key"

# Создаем экземпляр класса для хранения паролей
pwd_context = CryptContext(schemes=["bcrypt"])

# Создаем экземпляр класса HTTPBearer для проверки токена авторизации
bearer = HTTPBearer()

# Пример данных пользователей
USERS = [
    {"username": "admin", "password": "$2b$12$TpLt3BSS/7KaiU8zF1lXYODZD.mupmFsBkt1.YVb7jvv1UAv0rTXK"},
    {"username": "user", "password": "$2b$12$caRJxqy8r0YI6hEPaSStcultkX59tCCVXGEt8KksvYmwJKC0CBQdy"},
]


# Защищенный маршрут, который требует JWT авторизации
@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        # Проверяем и декодируем токен
        payload = decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=403, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

    return {"message": "Hello, {}".format(username)}


# Маршрут для аутентификации пользователя и генерации токена
@app.post("/login")
def login(username: str, password: str):
    user = next((user for user in USERS if user["username"] == username), None)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(username)
    return {"access_token": token}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username):
    payload = {"sub": username}
    token = encode(payload, SECRET_KEY, algorithm="HS256")
    return token