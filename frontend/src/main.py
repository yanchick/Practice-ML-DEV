from datetime import datetime

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dash_table, dcc

from src.requests import Requests

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

# Global variable to track login status (for demonstration purposes)
# In a production app, use a more secure method for session management
is_logged_in = False


# Define the layout of the app
app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)
