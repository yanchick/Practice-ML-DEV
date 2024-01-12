import dash
import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, callback

from src.requests import api



dash.register_page(
    __name__,
    path="/login",
)

layout = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        html.Div(
                            [
                                dbc.Input(id="login_username", placeholder="Username", type="text", className="mb-3"),
                                dbc.Input(
                                    id="login_password",
                                    placeholder="Password",
                                    type="password",
                                    className="mb-3",
                                ),
                                dbc.Button("Login", id="login_button", n_clicks=0),
                            ]
                        )
                    ],
                    label="Login",
                ),
                dbc.Tab(
                    [
                        html.Div(
                            [
                                dbc.Input(id="signup_username", placeholder="Username", type="text", className="mb-3"),
                                dbc.Input(
                                    id="signup_password",
                                    placeholder="Password",
                                    type="password",
                                    className="mb-3",
                                ),
                                dbc.Input(
                                    id="signup_repeat_password",
                                    placeholder="Repeat Password",
                                    type="password",
                                    className="mb-3",
                                ),
                                dbc.Button("Signup", id="signup_button", n_clicks=0),
                            ]
                        )
                    ],
                    label="Signup",
                ),
            ]
        ),
        html.Div(id="output_container"),
    ]
)

@callback(  # type: ignore
    Output("output_container", "children", allow_duplicate=True),
    Input("login_button", "n_clicks"),
    State("login_username", "value"),
    State("login_password", "value"),
    prevent_initial_call=True,
)
def handle_login(n_clicks: int, username: str, password: str) -> html.Div:
    global is_logged_in
    if n_clicks > 0:
        # Placeholder for API call: verify_user(username, password)
        # Replace with actual API call and handle the response
        api.login(username, password)
        is_logged_in = True  # Update based on actual verification result
        return html.Div([html.H3("Welcome to the Main Page"), html.Button("Logout", id="logout_button")])


@callback(  # type: ignore
    Output("output_container", "children", allow_duplicate=True),
    Input("signup_button", "n_clicks"),
    State("signup_username", "value"),
    State("signup_password", "value"),
    State("signup_repeat_password", "value"),
    prevent_initial_call=True,
)
def handle_signup(n_clicks: int, username: str, password: str, repeat_password: str) -> html.Div:
    global is_logged_in
    if n_clicks > 0 and password == repeat_password:
        # Placeholder for API call: create_user(username, password)
        # Replace with actual API call and handle the response
        api.signup(username, password)
        is_logged_in = True  # Update based on actual verification result
        return html.Div([html.H3("Welcome to the Main Page"), html.Button("Logout", id="logout_button")])
