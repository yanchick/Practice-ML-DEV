import dash
from dash import dcc, html

from frontend.callbacks.callbacks import register_callbacks
from frontend.ui_kit.styles import page_content_style

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Interval(id='interval-component', interval=5 * 60 * 1000),
    dcc.Store(id='user-session', storage_type='session'),

    dcc.Store(id='sign-in-session-update', storage_type='session'),
    dcc.Store(id='sign-up-session-update', storage_type='session'),

    html.Div(id='nav-bar'),
    html.Div(id='page-content', style=page_content_style)
])

if __name__ == '__main__':
    register_callbacks(app)
    app.run(debug=True, host='0.0.0.0', port=9000)
