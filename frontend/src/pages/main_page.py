from typing import Any

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, dcc, html

from src.api_client.models import ModelScheme
from src.requests import api

dash.register_page(__name__, path="/main")

models: list[ModelScheme] = []
if len(models) == 0:
    models = api.get_models()


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            # User info and balance
                            html.Div(id="user-info"),
                            # Input field for data
                            dcc.Input(id="input-data", type="text", placeholder="Enter data..."),
                            # Dropdown for model selection
                            dcc.Dropdown(
                                [model.name for model in models],
                                models[0].name if len(models) > 0 else "",
                                id="model-dropdown"
                            ),
                            # Submit button
                            html.Button("Submit", id="submit-button", n_clicks=0),
                            html.Div(id="submit-status"),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            # Table for history of predictions
                            dash_table.DataTable(id="predictions-table"),
                            # Button for updating table
                            html.Button("Update History", id="update-button", n_clicks=0),
                        ]
                    ),
                    width=6,
                ),
            ]
        )
    ],
    fluid=True,
)


# Callback to update user info
@callback(Output("user-info", "children"), [Input("submit-button", "n_clicks"), Input("update-button", "n_clicks")])  # type: ignore[misc]
def update_user_info(n1: Any, n2: Any) -> str:
    user = api.me()
    if user is not None:
        return f"Username: {user.username}, Balance: {user.balance}"
    return "Not logged in"


columns = ["Prediction ID", "Prediction Data", "Model Name", "Result"]


# Callback to update the predictions table
@callback(  # type: ignore[misc]
    Output("predictions-table", "columns"), Output("predictions-table", "data"), Input("update-button", "n_clicks")
)
def update_predictions_table(n_clicks: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    predictions = api.get_user_predictions()
    if predictions:
        # Transform predictions data into a format suitable for the DataTable
        data = [
            {
                "Prediction ID": pred.id,
                "Prediction Data": pred.input_data,
                "Model Name": pred.predicted_model_id,
                "Result": pred.result,
            }
            for pred in predictions.predictions
        ]

        # Define the table columns
        columns = [{"name": col, "id": col} for col in data[0].keys()]

        return columns, data
    return [], []


@callback(  # type: ignore[misc]
    Output("submit-status", "children"),  # Output to display the status of submission
    Input("submit-button", "n_clicks"),  # Triggered by the submit button click
    State("input-data", "value"),  # Gets the value entered in the input field
    State("model-dropdown", "value"),  # Gets the selected model from the dropdown
)
def submit_prediction_data(n_clicks: int, input_data: str, model_name: str) -> str:
    if n_clicks > 0 and input_data and model_name:
        success = api.post_prediction(data=[input_data], model_name=model_name)
        if success:
            return "Prediction submitted successfully."
        else:
            return "Failed to submit prediction."
    return ""
