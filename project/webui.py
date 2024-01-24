from dash import Dash, html, dcc, Input, Output, State
import requests
from dash.exceptions import PreventUpdate
from dash import callback_context

# Initialize Dash app
app = Dash(__name__)

# Define layout
# Define layout
# Define layout
app.layout = html.Div(
    [
        html.H1("Сервис по предсказанию возрастной группы"),
        dcc.Input(id="feature1", type="number", placeholder="Введите RIAGENDR"),
        dcc.Input(id="feature2", type="number", placeholder="Введите PAQ605"),
        dcc.Input(id="feature3", type="number", placeholder="Введите BMXBMI"),
        dcc.Input(id="feature4", type="number", placeholder="Введите LBXGLU"),
        dcc.Input(id="feature5", type="number", placeholder="Введите DIQ010"),
        dcc.Input(id="feature6", type="number", placeholder="Введите LBXGLT"),
        dcc.Input(id="feature7", type="number", placeholder="Введите LBXIN"),
        html.Button("Предсказать", id="submit-button"),
        html.Br(),  # Add line break
        html.Div(id="output-message", style={"margin-top": "20px"}),  # Add margin
        html.Div(id="hidden-prediction-id", style={"display": "none"}),  # Hidden div to store prediction ID
        html.Br(),  # Add line break
        dcc.Input(id="prediction-id", type="number", placeholder="Введите ID"),
        html.Button("Результат", id="get-prediction-button"),
        html.Br(),  # Add line break
        html.Div(id="predictions-output", style={"margin-top": "20px"})  # Add margin
    ]
)



# Define callback to interact with FastAPI
@app.callback(
    [
        Output("output-message", "children"),
        Output("hidden-prediction-id", "children"),
        Output("predictions-output", "children"),
    ],
    [
        Input("submit-button", "n_clicks"),
        Input("get-prediction-button", "n_clicks"),
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

    if triggered_id == "submit-button":
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

        # Call FastAPI endpoint to upload data
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

            # Return both the output message and the stored prediction ID
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


    elif triggered_id == "get-prediction-button" and prediction_id is not None:

        # Call FastAPI endpoint to get predictions using the provided prediction ID

        predictions_response = requests.get(f"http://127.0.0.1:8000/get-prediction-result/{int(prediction_id)}")

        if predictions_response.status_code == 200:

            # Extract the prediction result directly

            prediction_result = predictions_response.json().get("prediction_result", "No prediction result")

            predictions = f"Результат предсказания: {prediction_result}"

        else:

            predictions = f"Failed to fetch predictions. Status code: {predictions_response.status_code}"

        # Return the predictions

        return None, None, predictions

if __name__ == "__main__":
    app.run_server(debug=True)
