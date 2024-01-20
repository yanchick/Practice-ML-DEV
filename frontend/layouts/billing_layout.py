from dash import dash_table, dcc, html
from dash.dash_table.Format import Format, Group

from frontend.data.remote_data import fetch_transaction_history, fetch_user_balance
from frontend.ui_kit.components.user_balance import user_balance
from frontend.ui_kit.styles import table_style, table_header_style, table_cell_style, primary_button_style, \
    text_style, input_style
from frontend.ui_kit.utils import format_timestamp


# Components
def deposit_form():
    return html.Div([
        dcc.Input(
            id="deposit-amount",
            type="number",
            placeholder="Amount",
            value="",
            style=input_style
        ),
        html.Button(
            "Deposit",
            id="deposit-button",
            n_clicks=0,
            style=primary_button_style
        ),
    ], style={'display': 'flex', 'alignItems': 'center'})


def transaction_history_table(transactions):
    data = [{"id": txn["id"],
             "amount": txn["amount"],
             "timestamp": format_timestamp(txn["timestamp"])} for txn in transactions]
    if not data:
        return html.Div("No transactions to display", style=text_style)

    columns = [
        {"name": "Amount", "id": "amount", "type": "numeric", "format": Format(group=Group.yes)},
        {"name": "Timestamp", "id": "timestamp"}
    ]

    return dash_table.DataTable(
        columns=columns,
        data=data,
        style_table=table_style,
        style_cell=table_cell_style,
        style_header=table_header_style
    )


# Layout
def billing_layout(user_session):
    transactions = fetch_transaction_history(user_session=user_session)
    balance = fetch_user_balance(user_session)
    return html.Div([
        html.Div(user_balance(balance), id='current-balance-billing'),
        deposit_form(),
        html.Div(transaction_history_table(transactions), id='transaction-history-table'),
    ])
