# Импорт библиотек
import dash
from dash import dcc, html, callback, Output, Input, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def register_user(username, password, name, surname):
    register_url = "http://127.0.0.1/register"
    print(username)
    data = {
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
    }

    try:
        response = requests.post(register_url, json=data)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()
    except requests.HTTPError as e:
        return {"error": f"Registration failed: {str(e)}"}


# Заглушка для вызова FastAPI-функции входа пользователя
def login_user(username, password):
    # Здесь должен быть вызов FastAPI-функции для авторизации
    return {"access_token": "dummy_token", "token_type": "bearer"}


def get_history(access_token):
    # Здесь должен быть вызов FastAPI-функции для получения истории запросов
    return {"history": ["Request 1", "Request 2", "Request 3"]}


app.layout = html.Div(
    [
        html.H1("Определение возраста по медицинским данным"),
        html.Div(
            [
                html.H2("Login"),
                dcc.Input(
                    id="login-username", type="text", placeholder="Username"
                ),
                dcc.Input(
                    id="login-password",
                    type="password",
                    placeholder="Password",
                ),
                html.Button("Login", id="btn-login"),
            ]
        ),
        html.Div(id="output-login"),
        html.Div(
            [
                html.H2("Registration"),
                dcc.Input(
                    id="reg-username", type="text", placeholder="Username"
                ),
                dcc.Input(
                    id="reg-password", type="password", placeholder="Password"
                ),
                dcc.Input(id="reg-name", type="text", placeholder="Name"),
                dcc.Input(
                    id="reg-surname", type="text", placeholder="Surname"
                ),
                html.Button("Register", id="btn-register"),
            ]
        ),
        html.Div(id="output-reg"),
        html.H2("Введите модель для инференса:"),
        dcc.Dropdown(
            id="dropdown-model",
            options=[
                {
                    "label": "LinearRegression",
                    "value": 0,
                },
                {
                    "label": "DecisionTreeRegressor",
                    "value": 1,
                },
                {
                    "label": "KNeighborsRegressor",
                    "value": 2,
                },
            ],
            value=None,
        ),
        html.H2("Введите данные для модели, которая определит Ваш возраст:"),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Человек старше 65 лет?"),
                                dcc.Checklist(
                                    id="checkbox-age",
                                    options=[{"label": "Да", "value": "yes"}],
                                    value=[],
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label("Мужчина или женщина?"),
                                dcc.Dropdown(
                                    id="dropdown-gender",
                                    options=[
                                        {
                                            "label": "Мужчина",
                                            "value": "male",
                                        },
                                        {
                                            "label": "Женщина",
                                            "value": "female",
                                        },
                                    ],
                                    value=None,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Сколько дней в неделю занимались спортом?"
                                ),
                                dcc.Dropdown(
                                    id="dropdown-sport-days",
                                    options=[
                                        {"label": str(i), "value": i}
                                        for i in range(1, 8)
                                    ],
                                    value=None,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label("Индекс массы тела (BMI)"),
                                dcc.Slider(
                                    id="slider-bmi",
                                    min=14.5,
                                    max=70,
                                    step=0.1,
                                    value=None,
                                    marks={
                                        i: str(i) for i in range(15, 71, 5)
                                    },
                                ),
                                html.Div(id="slider-bmi-value"),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label(
                                    "Уровень глюкозы в крови после голодания"
                                ),
                                dcc.Slider(
                                    id="slider-glucose",
                                    min=63,
                                    max=405,
                                    step=1,
                                    value=None,
                                    marks={
                                        i: str(i) for i in range(70, 406, 50)
                                    },
                                ),
                                html.Div(id="slider-glucose-value"),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label("Степень диабета"),
                                dcc.Dropdown(
                                    id="dropdown-diabetes-degree",
                                    options=[
                                        {"label": "1", "value": 1},
                                        {"label": "2", "value": 2},
                                        {"label": "3", "value": 3},
                                    ],
                                    value=None,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label("Уровень гемоглобина"),
                                dcc.Slider(
                                    id="slider-hemoglobin",
                                    min=40,
                                    max=604,
                                    step=1,
                                    value=None,
                                    marks={
                                        i: str(i) for i in range(50, 605, 50)
                                    },
                                ),
                                html.Div(id="slider-hemoglobin-value"),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Label("Уровень инсулина в крови"),
                                dcc.Slider(
                                    id="slider-insulin",
                                    min=1,
                                    max=102,
                                    step=1,
                                    value=None,
                                    marks={
                                        i: str(i) for i in range(10, 103, 10)
                                    },
                                ),
                                html.Div(id="slider-insulin-value"),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Button("Получить данные", id="btn-get-data"),
        html.Button("Получить результат сетки", id="btn-get-result"),
        html.Div(id="output-data"),
        html.Div(id="output-result"),
        html.Div(
            [
                html.H3("История запросов:"),
                html.Ul(id="history-list"),
            ]
        ),
    ]
)


@app.callback(
    Output("output-reg", "children"),
    [Input("btn-register", "n_clicks")],
    [
        State("reg-username", "value"),
        State("reg-password", "value"),
        State("reg-name", "value"),
        State("reg-surname", "value"),
    ],
)
def register_callback(n_clicks, username, password, name, surname):
    if n_clicks is None:
        raise PreventUpdate
    print(username)
    response = register_user(username, password, name, surname)
    message = response.get("message", "Registration failed")

    history_response = get_history(access_token="dummy_token")
    history = history_response.get("history", [])

    # Обновляем текстовое поле с историей запросов
    return [html.Li(f"Registration: {message}")] + [
        html.Li(f"Request History: {h}") for h in history
    ]


@app.callback(
    Output("output-login", "children"),
    [Input("btn-login", "n_clicks")],
    [State("login-username", "value"), State("login-password", "value")],
)
def login_callback(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate

    response = login_user(username, password)
    access_token = response.get("access_token", "")

    # Получаем историю запросов
    history_response = get_history(access_token=access_token)
    history = history_response.get("history", [])
    return [html.Li(f"Login: Access Token: {access_token}")] + [
        html.Li(f"Request History: {h}") for h in history
    ]


@app.callback(
    [
        Output(f"slider-{field}-value", "children")
        for field in ["bmi", "glucose", "hemoglobin", "insulin"]
    ],
    [
        Input(f"slider-{field}", "value")
        for field in ["bmi", "glucose", "hemoglobin", "insulin"]
    ],
)
def update_slider_values(bmi, glucose, hemoglobin, insulin):
    return [
        f"Текущее значение: {value}"
        for value in [bmi, glucose, hemoglobin, insulin]
    ]


@app.callback(
    Output("output-data", "children"),
    Input("btn-get-data", "n_clicks"),
    State("dropdown-model", "value"),
    State("checkbox-age", "value"),
    State("dropdown-gender", "value"),
    State("dropdown-sport-days", "value"),
    State("slider-bmi", "value"),
    State("slider-glucose", "value"),
    State("dropdown-diabetes-degree", "value"),
    State("slider-hemoglobin", "value"),
    State("slider-insulin", "value"),
)
def get_and_display_data(
    n_clicks,
    model,
    age,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    data_str = f"Model: {model},Age: {age}, Gender: {gender}, Sport Days: {sport_days}, BMI: {bmi}, Glucose: {glucose}, Diabetes Degree: {diabetes_degree}, Hemoglobin: {hemoglobin}, Insulin: {insulin}"

    return html.Div(data_str)


def check_data(
    model,
    age,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
):
    error_responce = "Invalid data"
    model = model
    print(age)
    age = 0 if len(age) == 0 else 1
    if gender:
        gender = 0 if gender == "male" else 1
    else:
        return error_responce
    if sport_days:
        sport_days = sport_days
    else:
        return error_responce
    if bmi:
        bmi = bmi
    else:
        return error_responce
    if glucose:
        glucose = glucose
    else:
        return error_responce
    if diabetes_degree:
        diabetes_degree = diabetes_degree
    else:
        return error_responce
    if hemoglobin:
        hemoglobin = hemoglobin
    else:
        return error_responce
    if insulin:
        insulin = insulin
    else:
        return error_responce
    return (
        model,
        age,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
    )


@app.callback(
    [Output("history-list", "children")],
    Input("btn-get-result", "n_clicks"),
    State("dropdown-model", "value"),
    State("checkbox-age", "value"),
    State("dropdown-gender", "value"),
    State("dropdown-sport-days", "value"),
    State("slider-bmi", "value"),
    State("slider-glucose", "value"),
    State("dropdown-diabetes-degree", "value"),
    State("slider-hemoglobin", "value"),
    State("slider-insulin", "value"),
)
def update_result(
    n_clicks,
    model,
    age,
    gender,
    sport_days,
    bmi,
    glucose,
    diabetes_degree,
    hemoglobin,
    insulin,
):
    checked_data = check_data(
        model,
        age,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
    )

    if n_clicks is None:
        return dash.no_update, dash.no_update

    if checked_data == "Invalid data":
        return html.Div("Invalid data"), dash.no_update
    else:
        (
            model,
            age,
            gender,
            sport_days,
            bmi,
            glucose,
            diabetes_degree,
            hemoglobin,
            insulin,
        ) = checked_data
        print(checked_data)
        inference_server_url = "http://127.0.0.1:8936/predict"
        data = {
            "model": model,
            "age_group": age,
            "RIAGENDR": gender,
            "PAQ605": sport_days,
            "BMXBMI": bmi,
            "LBXGLU": glucose,
            "DIQ010": diabetes_degree,
            "LBXGLT": hemoglobin,
            "LBXIN": insulin,
        }

        response = requests.post(inference_server_url, json=data)

        # Обработка результата
        if response.status_code == 200:
            print(response)
            print(response.json())
            result = response.json()["prediction"]
            result_message = f"Результат предсказания: {result}"

            # Добавление запроса в историю
            history_item = html.Li(
                f"Model: {model}, Запрос: Старше 65?={age}, Gender={gender}, Sport Days={sport_days}, BMI={bmi}, Glucose={glucose}, Diabetes Degree={diabetes_degree}, Hemoglobin={hemoglobin}, Insulin={insulin}, Результат: {result}"
            )

            return result_message, [history_item]
        else:
            return "Ошибка при отправке запроса", dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
