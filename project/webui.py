from dash import Dash, html, dcc, Input, Output, State
import requests
from dash.exceptions import PreventUpdate
from dash import callback_context


app = Dash(__name__)


app.layout = html.Div(
    [
        html.Div(id="login-register", children=[
            dcc.Input(id="username", type="text", placeholder="Enter username"),
            dcc.Input(id="password", type="password", placeholder="Enter password"),
            html.Button("Sign In", id="sign-in-button"),
            html.Button("Register", id="register-button"),
            html.Div(id="login-message"),
        ]),
        html.Div(id="prediction-service", style={"display": "none"}, children=[
            html.H1("Prediction Service"),
            dcc.Input(id="feature1", type="number", placeholder="Enter RIAGENDR"),
            dcc.Input(id="feature2", type="number", placeholder="Enter PAQ605"),
            dcc.Input(id="feature3", type="number", placeholder="Enter BMXBMI"),
            dcc.Input(id="feature4", type="number", placeholder="Enter LBXGLU"),
            dcc.Input(id="feature5", type="number", placeholder="Enter DIQ010"),
            dcc.Input(id="feature6", type="number", placeholder="Enter LBXGLT"),
            dcc.Input(id="feature7", type="number", placeholder="Enter LBXIN"),
            html.Button("Predict", id="predict-button"),
            html.Br(),
            html.Div(id="output-message", style={"margin-top": "20px"}),
            html.Div(id="hidden-prediction-id", style={"display": "none"}),
            html.Br(),
            dcc.Input(id="prediction-id", type="number", placeholder="Enter ID"),
            html.Button("Get Result", id="get-result-button"),
            html.Br(),
            html.Div(id="predictions-output", style={"margin-top": "20px"})
        ])
    ]
)



@app.callback(
    Output("login-message", "children"),
    Output("prediction-service", "style"),
    Input("sign-in-button", "n_clicks"),
    Input("register-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def authenticate_user(sign_in_clicks, register_clicks, username, password):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    triggered_id = ctx.triggered_id.split(".")[0]

    if triggered_id == "register-button":
        response = requests.post(
            "http://127.0.0.1:8000/sign-up",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return "Registration successful! You can now sign in.", {"display": "block"}
        else:
            return "Registration failed. Please try again.", {"display": "none"}

    elif triggered_id == "sign-in-button":
        response = requests.post(
            "http://127.0.0.1:8000/sign-in",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return "Welcome! You are now signed in.", {"display": "block"}
        else:
            return "Invalid username or password. Please try again.", {"display": "none"}




@app.callback(
    [
        Output("output-message", "children"),
        Output("hidden-prediction-id", "children"),
        Output("predictions-output", "children"),
    ],
    [
        Input("predict-button", "n_clicks"),
        Input("get-result-button", "n_clicks"),
    ],
    [
        State("feature1", "value"),
        State("feature2", "value"),
        State("feature3", "value"),
        State("feature4", "value"),
        State("feature5", "value"),
        State("feature6", "value"),
        State("feature7", "value"),
        State("prediction-id", "value"),
    ],
)
def make_and_get_predictions(
    submit_n_clicks, get_prediction_n_clicks,
    feature1, feature2, feature3, feature4, feature5, feature6, feature7, prediction_id
):
    ctx = callback_context
    if not ctx.triggered_id:
        raise PreventUpdate

    triggered_id = ctx.triggered_id.split(".")[0]

    if triggered_id == "predict-button":
        try:
            feature1 = float(feature1)
            feature2 = float(feature2)
            feature3 = float(feature3)
            feature4 = float(feature4)
            feature5 = float(feature5)
            feature6 = float(feature6)
            feature7 = float(feature7)
        except ValueError:
            return "Invalid input. Please enter numeric values for features.", None, None


        response = requests.post(
            "http://127.0.0.1:8000/upload-data",
            json={
                "RIAGENDR": feature1,
                "PAQ605": feature2,
                "BMXBMI": feature3,
                "LBXGLU": feature4,
                "DIQ010": feature5,
                "LBXGLT": feature6,
                "LBXIN": feature7,
            },
        )

        if response.status_code == 200:
            result = response.json()
            prediction_result = result.get("prediction_result", "No prediction result")
            prediction_id = result.get("id")


            return (
                f"Данные успешно загружены. Выполняется предсказание. Чтобы получить результат, введите номер ID и нажмите кнопку 'Результат'. ID: {prediction_id}",
                prediction_id,
                None
            )
        else:
            return (
                f"Failed to upload data. Status code: {response.status_code}",
                None,
                None
            )


    elif triggered_id == "get-result-button" and prediction_id is not None:
        predictions_response = requests.get(f"http://127.0.0.1:8000/get-prediction-result/{int(prediction_id)}")

        if predictions_response.status_code == 200:
            prediction_result = predictions_response.json().get("prediction_result", "No prediction result")
            predictions = f"Результат предсказания: {prediction_result}"
        else:
            predictions = f"Failed to fetch predictions. Status code: {predictions_response.status_code}"
        return None, None, predictions

if __name__ == "__main__":
    app.run_server(debug=True)
