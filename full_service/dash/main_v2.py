import dash
from dash import dcc, html, callback, Output, Input, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ac_token = None

app.layout = html.Div(
    [
        html.H1("Аутентификация и авторизация с Dash и FastAPI"),
        html.Div(
            [
                html.H2("Регистрация"),
                dcc.Input(
                    id="reg-username",
                    type="text",
                    placeholder="Username",
                ),
                dcc.Input(
                    id="reg-password", type="password", placeholder="Пароль"
                ),
                dcc.Input(
                    id="reg-surname",
                    type="text",
                    placeholder="Фамилия пользователя",
                ),
                dcc.Input(
                    id="reg-name",
                    type="text",
                    placeholder="Имя пользователя",
                ),
                html.Button("Зарегистрироваться", id="btn-register"),
                html.Div(id="output-register"),
            ]
        ),
        html.Div(
            [
                html.H2("Авторизация"),
                dcc.Input(
                    id="login-username",
                    type="text",
                    placeholder="Имя пользователя",
                ),
                dcc.Input(
                    id="login-password", type="password", placeholder="Пароль"
                ),
                html.Button("Войти", id="btn-login"),
                html.Div(id="output-login"),
            ]
        ),
        html.Div(
            [
                html.H2("Пример использования токена"),
                dcc.Input(
                    id="token-input",
                    type="text",
                    placeholder="Введите JWT токен",
                ),
                html.Button("Проверить токен", id="btn-check-token"),
                html.Div(id="output-token"),
            ]
        ),
        dcc.Store(id="token-store"),
    ]
)


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
        return f"Registration failed: {str(e)}"


# Callback для авторизации
@app.callback(
    [Output("token-store", "data")],
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
        return [access_token]
    except requests.HTTPError as e:
        return [None]


# Callback для использования токена
@app.callback(
    Output("output-token", "data"),
    [Input("btn-check-token", "n_clicks")],
    [State("token-store", "data")],
)
def check_token_callback(n_clicks, token):
    print(token)
    if n_clicks is None:
        raise PreventUpdate

    check_token_url = "http://127.0.0.1:8935/user/predict_rows"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(check_token_url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса
        return f"Token is valid"
    except requests.HTTPError as e:
        return f"Token check failed: {str(e)}"


if __name__ == "__main__":
    app.run_server(debug=True)
