import dash
from dash import Response
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

def login(username, password):
    # Здесь должна быть ваша логика для авторизации через внешний сервис по HTTP.
    # Вместо примера сделаем простую проверку с использованием заглушки в виде запроса на фейковый сервер.
    return True
    response = requests.post('http://fake-server.com/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        return True
    else:
        return False

app.layout = html.Div([
    html.H1('Приложение авторизации'),
    html.Div([
        html.Label('Имя пользователя'),
        dcc.Input(id='username', type='text')
    ]),
    html.Div([
        html.Label('Пароль'),
        dcc.Input(id='password', type='password')
    ]),
    html.Button('Войти', id='login-button', n_clicks=0),
    html.Div(id='login-status')
])

@app.callback(
    Output('login-status', 'children'),
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')])
def authenticate(n_clicks, username, password):
    if n_clicks > 0:
        if login(username, password):
            response = Response()
            response.headers['Content-Type'] = 'application/json'
            return html.Div([
                html.H3(f'Добро пожаловать, {username}!'),
                dcc.Location(id='url', refresh=True),
                html.Div([
                    dcc.Link('Страница 1', href='/page1'),
                    html.Br(),
                    dcc.Link('Страница 2', href='/page2'),
                    html.Br(),
                    dcc.Link('Страница 3', href='/page3')
                ], className='sidebar-menu')
            ])
        else:
            return html.Div('Ошибка авторизации. Попробуйте снова.')

@app.callback(Output('url', 'pathname'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return html.H1('Страница 1')
    elif pathname == '/page2':
        return html.H1('Страница 2')
    elif pathname == '/page3':
        return html.H1('Страница 3')

if __name__ == '__main__':
    app.run_server(debug=True)
