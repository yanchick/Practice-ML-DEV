import dash
from dash import dcc, html, callback, Output, Input, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests
from config import model_id2name, gender2gender_name, cell_style


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.prevent_initial_callbacks = "initial_duplicate"

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Регистрация"),
                            dbc.Col(
                                [
                                    html.Div(
                                        dcc.Input(
                                            id="reg-username",
                                            type="text",
                                            placeholder="Username",
                                        )
                                    ),
                                    html.Div(
                                        dcc.Input(
                                            id="reg-password",
                                            type="password",
                                            placeholder="Пароль",
                                        )
                                    ),
                                    html.Div(
                                        dcc.Input(
                                            id="reg-surname",
                                            type="text",
                                            placeholder="Фамилия пользователя",
                                        )
                                    ),
                                    html.Div(
                                        dcc.Input(
                                            id="reg-name",
                                            type="text",
                                            placeholder="Имя пользователя",
                                        )
                                    ),
                                    html.Button(
                                        "Зарегистрироваться", id="btn-register"
                                    ),
                                    html.Div(id="output-register"),
                                ]
                            ),
                        ]
                    ),
                    width="auto",
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Авторизация"),
                            dbc.Col(
                                [
                                    html.Div(
                                        dcc.Input(
                                            id="login-username",
                                            type="text",
                                            placeholder="Имя пользователя",
                                        )
                                    ),
                                    html.Div(
                                        dcc.Input(
                                            id="login-password",
                                            type="password",
                                            placeholder="Пароль",
                                        )
                                    ),
                                    html.Button("Войти", id="btn-login"),
                                    html.Div(id="output-login"),
                                ]
                            ),
                        ],
                    ),
                    width="auto",
                ),
            ],
            id="first-block-div",
            style={"display": ""},
        ),
        html.Div(
            [
                html.H1("Ваш счет:"),
                html.H1("Авторизация не пройдена", id="score-div"),
                dcc.Interval(
                    id="interval-component",
                    interval=1300,  # in milliseconds
                    n_intervals=0,
                ),
                dcc.Store(id="token-store"),
                html.H2("Введите модель для инференса:"),
                dcc.Dropdown(
                    id="dropdown-model",
                    options=[
                        {
                            "label": "LinearRegression 10 points",
                            "value": 0,
                        },
                        {
                            "label": "DecisionTreeRegressor 15 points",
                            "value": 1,
                        },
                        {
                            "label": "KNeighborsRegressor 20 points",
                            "value": 2,
                        },
                    ],
                    value=None,
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "Введите данные для модели, которая определит Ваш возраст:"
                                ),
                                html.Div(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Человек старше 65 лет?"
                                                        ),
                                                        dcc.Checklist(
                                                            id="checkbox-age",
                                                            options=[
                                                                {
                                                                    "label": "Да",
                                                                    "value": "yes",
                                                                }
                                                            ],
                                                            value=[],
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Мужчина или женщина?"
                                                        ),
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
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Сколько дней в неделю занимались спортом?"
                                                        ),
                                                        dcc.Dropdown(
                                                            id="dropdown-sport-days",
                                                            options=[
                                                                {
                                                                    "label": str(
                                                                        i
                                                                    ),
                                                                    "value": i,
                                                                }
                                                                for i in range(
                                                                    1, 8
                                                                )
                                                            ],
                                                            value=None,
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Индекс массы тела (BMI)"
                                                        ),
                                                        dcc.Slider(
                                                            id="slider-bmi",
                                                            min=14.5,
                                                            max=70,
                                                            step=0.1,
                                                            value=None,
                                                            marks={
                                                                i: str(i)
                                                                for i in range(
                                                                    15, 71, 5
                                                                )
                                                            },
                                                        ),
                                                        html.Div(
                                                            id="slider-bmi-value"
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
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
                                                                i: str(i)
                                                                for i in range(
                                                                    70, 406, 50
                                                                )
                                                            },
                                                        ),
                                                        html.Div(
                                                            id="slider-glucose-value"
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Степень диабета"
                                                        ),
                                                        dcc.Dropdown(
                                                            id="dropdown-diabetes-degree",
                                                            options=[
                                                                {
                                                                    "label": "1",
                                                                    "value": 1,
                                                                },
                                                                {
                                                                    "label": "2",
                                                                    "value": 2,
                                                                },
                                                                {
                                                                    "label": "3",
                                                                    "value": 3,
                                                                },
                                                            ],
                                                            value=None,
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Уровень гемоглобина"
                                                        ),
                                                        dcc.Slider(
                                                            id="slider-hemoglobin",
                                                            min=40,
                                                            max=604,
                                                            step=1,
                                                            value=None,
                                                            marks={
                                                                i: str(i)
                                                                for i in range(
                                                                    50, 605, 50
                                                                )
                                                            },
                                                        ),
                                                        html.Div(
                                                            id="slider-hemoglobin-value"
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Label(
                                                            "Уровень инсулина в крови"
                                                        ),
                                                        dcc.Slider(
                                                            id="slider-insulin",
                                                            min=1,
                                                            max=102,
                                                            step=1,
                                                            value=None,
                                                            marks={
                                                                i: str(i)
                                                                for i in range(
                                                                    10, 103, 10
                                                                )
                                                            },
                                                        ),
                                                        html.Div(
                                                            id="slider-insulin-value"
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            width="auto",
                                        ),
                                    ]
                                ),
                                html.Button(
                                    "Получить данные", id="btn-get-data"
                                ),
                                html.Button(
                                    "Получить результат сетки",
                                    id="btn-get-result",
                                ),
                                html.Div(id="output-data"),
                                html.Div(id="output-result"),
                            ],
                            width="auto",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H3("История запросов:"),
                                        html.Table(id="history-table"),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ],
            id="second-block-div",
            style={"display": ""},
        ),
        dcc.Interval(
            id="interval-component-main",
            interval=1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)

# {
#   "age_group": 1,
#   "User_id": 4,
#   "sport_days": 2,
#   "glucose": 137,
#   "hemoglobin": 219,
#   "result": 75.66666666666667,
#   "id": 43,
#   "gender": 1,
#   "bmi": 28.9,
#   "diabetes_degree": 1,
#   "insulin": 33
# }


def create_cols_and_data_for_table(data):
    for x in range(len(data)):
        model = model_id2name[data[x]["model"]]
        age = "Старше 65" if data[x]["age_group"] == 1 else "Младше 65"
        data_instance = (
            model,
            age,
            gender2gender_name[data[x]["gender"]],
            data[x]["sport_days"],
            data[x]["bmi"],
            data[x]["glucose"],
            data[x]["diabetes_degree"],
            data[x]["hemoglobin"],
            data[x]["insulin"],
            data[x]["result"],
        )
        data[x] = data_instance
    return reversed(data)


def create_table(
    raw_data,
    keys=(
        "Модель",
        "Возрастная группа",
        "Пол",
        "Дни спорта",
        "ИМТ",
        "Глюкоза",
        "Уровень диабета",
        "Гемоглобин",
        "Инсулин",
        "Результат",
    ),
):
    data = create_cols_and_data_for_table(raw_data)
    table_rows = [
        html.Tr([html.Td(h, style=cell_style) for h in row]) for row in data
    ]
    table = html.Table(
        [
            html.Thead(html.Tr([html.Th(k) for k in keys])),
            html.Tbody(table_rows),
        ]
    )

    return table


def history_data_to_strings(data):
    for x in range(len(data)):
        data_instance = data[x]
        _ = "Младше 65" if data_instance["age_group"] == 1 else "Старше 65"
        data[
            x
        ] = f"Модель: {model_id2name[data_instance['model']]}, Запрос: {_}, Пол: {gender2gender_name[data_instance['gender']]}, Дней спорта поряд={data_instance['sport_days']}, ИМТ={data_instance['bmi']}, Глюкоза={data_instance['glucose']}, Уровень диабета={data_instance['diabetes_degree']}, Гемоглобин={data_instance['hemoglobin']}, Инсулин={data_instance['insulin']}, Результат: {round(data_instance['result'], 1)}"
    return reversed(data)


def get_history_list(
    history_url="http://127.0.0.1:8935/user/predict_rows", token=None
):
    headers = {"Authorization": f"{token}"}
    try:
        response = requests.get(history_url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса
        history_strings = history_data_to_strings(
            response.json()["predict_rows"]
        )
        return history_strings, response.json()["predict_rows"]
    except:
        return []


# Callback для регистрации
@app.callback(
    Output("output-register", "children"),
    [Input("btn-register", "n_clicks")],
    [
        State("reg-username", "value"),
        State("reg-password", "value"),
        State("reg-name", "value"),
        State("reg-surname", "value"),
    ],
)
def register_callback(
    n_clicks,
    username,
    password,
    name,
    surname,
):
    if n_clicks is None:
        raise PreventUpdate

    register_url = "http://127.0.0.1:8935/register"
    data = {
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
    }

    try:
        response = requests.post(register_url, json=data)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json().get("message", "Registration successfull")
    except requests.HTTPError as e:
        return "Registration failed: Probably registred already"


# Callback для авторизации
@app.callback(
    [
        Output("token-store", "data"),
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    [Input("btn-login", "n_clicks")],
    [
        State("login-username", "value"),
        State("login-password", "value"),
    ],
)
def login_callback(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate

    login_url = "http://127.0.0.1:8935/token"
    data = {
        "username": username,
        "password": password,
    }

    try:
        response = requests.post(login_url, data=data)
        response.raise_for_status()  # Проверяем успешность запроса
        access_token = response.json().get("access_token", "")
        hl, raw_data = get_history_list(token=access_token)
        return [access_token, create_table(raw_data)]
    except requests.HTTPError as e:
        return [None, html.Div("Не авторизован")]


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


@app.callback(
    [
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
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
    State("token-store", "data"),
)
def predict(
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
    token,
):
    if n_clicks is not None:
        fast_api_inference_url = "http://127.0.0.1:8935/send_data"
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
            "token": token,
        }
        try:
            response = requests.post(fast_api_inference_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return html.Div("Не авторизован")

        # Обработка результата
        try:
            hl, raw_data = get_history_list(token=token)
            return [create_table(raw_data)]
        except KeyError as e:
            return html.Div("Не авторизован")


@app.callback(
    [
        Output("score-div", "children"),
        Output("first-block-div", "style"),
        Output("second-block-div", "style"),
        Output(
            "history-table",
            "children",
            allow_duplicate=True,
        ),
    ],
    [Input("interval-component-main", "n_intervals")],
    State("token-store", "data"),
)
def update_score(n, token):
    bill_url = "http://127.0.0.1:8935/user/bill"
    headers = {"Authorization": f"{token}"}
    try:
        response = requests.get(bill_url, headers=headers)
        _, raw_data = get_history_list(token=token)
        response.raise_for_status()  # Проверяем успешность запроса
        return (
            response.json()["bill"],
            {"display": "none"},
            {"display": ""},
            create_table(raw_data),
        )
    except:
        return "Not authorized", {"display": ""}, {"display": "none"}, None


if __name__ == "__main__":
    app.run_server(debug=False)
