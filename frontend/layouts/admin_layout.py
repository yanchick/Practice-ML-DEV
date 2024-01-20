from dash import html, dash_table
from dash.dash_table.Format import Format, Group

from frontend.ui_kit.styles import table_style, table_header_style, table_cell_style, secondary_button_style, \
    text_style


# Components
def users_report(data):
    if not data:
        return html.Div("No information about users", style=text_style)

    columns = [
        {'name': 'Active Users', 'id': 'active_users', 'type': 'numeric'},
    ]

    data_array = [data]
    return dash_table.DataTable(columns=columns, data=data_array, style_table=table_style,
                                style_cell=table_cell_style,
                                style_header=table_header_style)


def predictions_report(data):
    if not data:
        return html.Div("No information about predictions", style=text_style)

    columns = [
        {'name': 'Model Name', 'id': 'model_name'},
        {'name': 'Total Predictions', 'id': 'total_prediction_batches', 'type': 'numeric',
         'format': Format(group=Group.yes)}
    ]
    return dash_table.DataTable(columns=columns, data=data, style_table=table_style,
                                style_cell=table_cell_style,
                                style_header=table_header_style)


def credits_report(data):
    if not data:
        return html.Div("No information about credits", style=text_style)

    columns = [
        {'name': 'Total Credits Purchased', 'id': 'total_credits_purchased', 'type': 'numeric'},
        {'name': 'Total Credits Spent', 'id': 'total_credits_spent', 'type': 'numeric'}
    ]

    data_array = [data]
    return dash_table.DataTable(columns=columns, data=data_array, style_table=table_style,
                                style_cell=table_cell_style,
                                style_header=table_header_style)


# Layout
def admin_layout():
    return html.Div(id='admin-page', children=[
        html.Div(id='users-report-div', children=users_report({})),
        html.Div(id='predictions-report-div', children=predictions_report([])),
        html.Div(id='credits-report-div', children=credits_report({})),
        html.Button("Refresh Data", id="refresh-button", n_clicks=0,
                    style={**secondary_button_style, 'display': 'block', 'margin': '0 auto', 'marginTop': '20px'}),
    ])
