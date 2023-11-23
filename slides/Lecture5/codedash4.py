from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
import dash
import dash_html_components as html

# Создание экземпляра FastAPI
app_fastapi = FastAPI()

# Создание экземпляра Dash
app_dash = dash.Dash(__name__)

# Маршрутизация FastAPI
@app_fastapi.get('/')
def home():
    return {'message': 'Привет, это FastAPI!'}

# Маршрутизация Dash
app_dash.layout = html.Div('Привет, это Dash!')

# Сконфигурируйте middleware WSGI для запуска Dash на FastAPI
middleware = WSGIMiddleware(app_dash.server)

# Подключите WSGIMiddleware в FastAPI
app_fastapi.add_middleware(middleware)

# Запуск FastAPI
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app_fastapi, host='0.0.0.0', port=8000)
