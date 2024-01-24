from dash import Dash, html, dcc, Input, Output
from dash.dependencies import State
import requests

# Initialize Dash app
app = Dash(__name__)

# Define layout
app.layout = html.Div(
    [
        html.H1("FastAPI + Dash Web UI"),
        dcc.Input(id="feature1", type="number", placeholder="Enter Feature 1"),
        dcc.Input(id="feature2", type="number", placeholder="Enter Feature 2"),
        dcc.Input(id="feature3", type="number", placeholder="Enter Feature 3"),
        dcc.Input(id="feature4", type="number", placeholder="Enter Feature 4"),
        dcc.Input(id="feature5", type="number", placeholder="Enter Feature 5"),
        dcc.Input(id="feature6", type="number", placeholder="Enter Feature 6"),
        dcc.Input(id="feature7", type="number", placeholder="Enter Feature 7"),
        html.Button("Submit", id="submit-button"),
        html.Div(id="output-message"),
        html.Div(id="predictions-output")  # Add a new HTML div for displaying predictions
    ]
)

# Define callback to interact with FastAPI
@app.callback(
    Output("output-message", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("feature1", "value"),
        State("feature2", "value"),
        State("feature3", "value"),
        State("feature4", "value"),
        State("feature5", "value"),
        State("feature6", "value"),
        State("feature7", "value"),
    ],
)
def make_prediction(
    n_clicks, feature1, feature2, feature3, feature4, feature5, feature6, feature7
):
    if n_clicks is not None:
        try:
            feature1 = float(feature1)
            feature2 = float(feature2)
            feature3 = float(feature3)
            feature4 = float(feature4)
            feature5 = float(feature5)
            feature6 = float(feature6)
            feature7 = float(feature7)
        except ValueError:
            return "Invalid input. Please enter numeric values for features."

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
            return f"Data uploaded successfully. Prediction result: {prediction_result}"
        else:
            return f"Failed to upload data. Status code: {response.status_code}"

# Callback to fetch predictions from FastAPI backend
@app.callback(
    Output("predictions-output", "children"),
    [Input("submit-button", "n_clicks")],  # You can use a button to trigger fetching predictions
)
def get_predictions(n_clicks):
    if n_clicks is not None:
        # Call FastAPI endpoint to get predictions
        response = requests.get("http://127.0.0.1:8000/get-predictions")

        if response.status_code == 200:
            predictions = response.json()
            # Display the predictions in the Dash app
            return f"Predictions: {predictions}"
        else:
            return f"Failed to fetch predictions. Status code: {response.status_code}"

if __name__ == "__main__":
    app.run_server(debug=True)
