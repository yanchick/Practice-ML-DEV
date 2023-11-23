from fastapi import FastAPI
import uvicorn
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

# Запуск FastAPI и Dash
if __name__ == '__main__':
    # Запуск FastAPI
    uvicorn.run(app_fastapi, host='0.0.0.0', port=8000)

    # Запуск Dash
    app_dash.run_server(debug=True)
