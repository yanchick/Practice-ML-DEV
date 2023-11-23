from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.wsgi import WSGIMiddleware
import dash
import flask
import dash_html_components as html

# Создание экземпляра FastAPI
app_fastapi = FastAPI()

# Создание экземпляров роутеров FastAPI и Dash
router_fastapi = APIRouter(prefix="/api")
router_dash = dash.Dash(__name__)

# Маршруты FastAPI
@router_fastapi.get('/')
def home():
    return JSONResponse(content={'message': 'Привет, это FastAPI!'},headers={'abc': '123'})

# Маршрутизация Dash
router_dash.layout = html.Div('Привет, это Dash!')

# Подключение роутеров к FastAPI
app_fastapi.include_router(router_fastapi)
app_fastapi.mount("/dashboard", WSGIMiddleware(router_dash.server))

# Запуск FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app_fastapi, host='0.0.0.0', port=8000)
