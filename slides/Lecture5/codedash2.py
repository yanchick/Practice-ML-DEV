import dash
import dash_table
import pandas as pd

app = dash.Dash(__name__)

# Подключение к базе данных и загрузка данных
data = pd.read_sql_query("SELECT * FROM my_table", db_connection)

app.layout = dash_table.DataTable(
    id='example-table',
    columns=[{"name": col, "id": col} for col in data.columns],
    data=data.to_dict('records')
)

if __name__ == '__main__':
    app.run_server(debug=True)
