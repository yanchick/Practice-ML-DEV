import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

def get_token():
    return 'axdd'

@server.after_request
def add_header(response):
    response.headers['Custom-Header'] = 'Custom Value'
    return response

app.layout = html.Div(
    children=[
        html.H1("Пример интерактивного графика"),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "График 1"},
                    {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "График 2"},
                ],
                "layout": {
                    "title": "Пример графика",
                    "xaxis": {"title": "Ось X"},
                    "yaxis": {"title": "Ось Y"},
                },
            },
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
