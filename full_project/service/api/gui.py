import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
from constants import CATEGORY_MAPPING

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
# FastAPI backend URL
FASTAPI_BACKEND_URL = "http://127.0.0.1:8000"

def layout_home():
    return dbc.Container([
        dbc.Row(dbc.Col(html.H1("Product Classification", className="text-center my-4"), width=12)),
        dbc.Row([
            dbc.Col(dbc.NavLink('Register', href='/register', className="btn btn-primary btn-lg", style={"padding": "10px 20px"}), width=3, className="my-2"),
            dbc.Col(dbc.NavLink('Login', href='/login', className="btn btn-secondary btn-lg", style={"padding": "10px 20px"}), width=3, className="my-2"),
            dbc.Col(dbc.NavLink('Predict', href='/predict', className="btn btn-success btn-lg", style={"padding": "10px 20px"}), width=3, className="my-2"),
            dbc.Col(dbc.NavLink('User Info', href='/user-info', className="btn btn-info btn-lg", style={"padding": "10px 20px"}), width=3, className="my-2"),
        ], justify="center"),
    ], fluid=True, style={"padding-top": "50px"})


# Layout for the registration page
def layout_register():
    return dbc.Container([
        dbc.Form([
            dbc.Input(id='reg_username', placeholder='Username'),
            dbc.Input(id='reg_password', placeholder='Password', type='password'),
            dbc.Button('Register', id='reg_button', color='primary'),
            html.Div(id='reg_status')
        ]),
        dcc.Link('Go back to Home', href='/')
    ])

# Layout for the login page
def layout_login():
    return dbc.Container([
        dbc.Form([
            dbc.Input(id='login_username', placeholder='Username'),
            dbc.Input(id='login_password', placeholder='Password', type='password'),
            dbc.Button('Login', id='login_button', color='primary'),
            html.Div(id='login_status')
        ]),
        dcc.Link('Go back to Home', href='/')
    ])

# Layout for the prediction page
def layout_predict():
    return dbc.Container([
        dbc.Form([
            dbc.Input(id='Product_Title', placeholder='Product_Title'),
            dbc.Input(id='Merchant_ID', placeholder='Merchant_ID'),
            dbc.Input(id='Cluster_ID', placeholder='Cluster_ID'),
            dbc.Input(id='Cluster_Label', placeholder='Cluster_Label'),
            # Add inputs for other features
            dbc.Select(
                id='model_selector',
                options=[
                    {'label': 'LightGBM', 'value': 'lgbm'},
                    {'label': 'Logistic Regression', 'value': 'logreg'},
                    {'label': 'Random Forest', 'value': 'randforest'}
                ]
            ),
            dbc.Button('Predict', id='predict_button', color='success'),
            html.Div(id='prediction_result')
        ]),
        dcc.Link('Go back to Home', href='/')
    ])

# In your layout_predict function or wherever you want to display the user info
def layout_user_info():
    return dbc.Container([
        dbc.Row(dbc.Col(html.Div(id="user-info-button"))),
        dcc.Link('Go back to Home', href='/')
    ])


# Main layout of the app
app.layout = dbc.Container([
    dcc.Store(id='auth-token', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('auth-token', 'data')])
def display_page(pathname, token):
    if pathname == '/register':
        return layout_register()
    elif pathname == '/login':
        return layout_login()
    elif pathname == '/predict':
        return layout_predict()
    elif pathname == '/user-info':
        return layout_user_info()  # Handle the user info page
    else:
        return layout_home()


# Callback for registration
@app.callback(
    Output('reg_status', 'children'),
    Input('reg_button', 'n_clicks'),
    [State('reg_username', 'value'), State('reg_password', 'value')],
    prevent_initial_call=True)
def register_user(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{FASTAPI_BACKEND_URL}/register", json={"username": username, "password": password})
        if response.status_code == 200:
            return "Registration Successful!"
        else:
            return "Username already registered!"

# Callback for login
@app.callback(
    Output('login_status', 'children'),
    Output('auth-token', 'data'),  # To store the token
    Input('login_button', 'n_clicks'),
    [State('login_username', 'value'), State('login_password', 'value')],
    prevent_initial_call=True)
def login_user(n_clicks, username, password):
    if n_clicks:
        response = requests.post(f"{FASTAPI_BACKEND_URL}/login", data={"username": username, "password": password})
        if response.status_code == 200:
            # Successful login
            access_token = response.json()["access_token"]
            return f"Login successfully.", access_token
        else:   
            # Failed login
            return "Incorrect username or password. Check your credentials.", None


@app.callback(
    Output('user-info-button', 'children'),
    [Input('url', 'pathname')],
    [State('auth-token', 'data')])
def get_user_info(pathname, token):
    if pathname == '/user-info' and token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{FASTAPI_BACKEND_URL}/user/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            jobs_list = [
                html.Li(f"Model: {job['model_name']}, Status: {job['status']}, Cost: {job['cost']}, Result: {job['result']}")
                for job in user_info['recent_jobs']
            ]
            return [
                html.P(f"{user_info['message']}, your balance is {user_info['balance']}"),
                html.Hr(),  # Horizontal line for separation
                html.H4("Recent Jobs:"),
                html.Ul(jobs_list)  # Unordered list of jobs
            ]
        else:
            return "Failed to fetch user info."
    return "Please login to view user info."


# Callback for prediction
@app.callback(
    Output('prediction_result', 'children'),
    [Input('predict_button', 'n_clicks'), State('auth-token', 'data')],
    [State('Product_Title', 'value'),
     State('Merchant_ID', 'value'),
     State('Cluster_ID', 'value'),
     State('Cluster_Label', 'value'),
     State('model_selector', 'value')],
    prevent_initial_call=True)
def make_prediction(n_clicks, token, Product_Title, Merchant_ID, Cluster_ID, Cluster_Label, model):
    if n_clicks and token:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "Product_Title": Product_Title,
            "Merchant_ID": Merchant_ID,
            "Cluster_ID": Cluster_ID,
            "Cluster_Label": Cluster_Label,
        }
        response = requests.post(f"{FASTAPI_BACKEND_URL}/predict/{model}", json=payload, headers=headers)
        if response.status_code == 200:
            category = response.json()['pred'][0]
            label = CATEGORY_MAPPING.get(category, "Unknown")
            balance = response.json()['balance']
            return [
                html.P(f"Category ID: {category}"),
                html.P(f"Category Label: {label}"),
                html.P(f"Current balance is {balance}")
            ]
        else:
            return "Prediction Failed!"
    return "Please login to make a prediction."



if __name__ == '__main__':
    app.run_server(debug=True)

