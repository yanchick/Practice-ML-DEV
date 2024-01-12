import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from time import sleep

sleep(2)  # to wait for the api to start

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div(
    [
        html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                html.Div(dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"]))
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
