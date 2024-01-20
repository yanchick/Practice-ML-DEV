import json
from datetime import datetime
from json import JSONDecodeError

from dash import Output, Input, State, callback_context, ALL, dcc
from dash.exceptions import PreventUpdate

from frontend.data.local_data import authentificated_session
from frontend.data.remote_data import fetch_predictions_reports, fetch_users_report, fetch_credits_report
from frontend.data.remote_data import fetch_transaction_history, deposit_amount, send_prediction_request, \
    fetch_prediction_history, register_user, fetch_models, authenticate_user, fetch_user_balance
from frontend.layouts.admin_layout import admin_layout
from frontend.layouts.admin_layout import users_report, predictions_report, credits_report
from frontend.layouts.billing_layout import billing_layout
from frontend.layouts.billing_layout import transaction_history_table
from frontend.layouts.prediction_layout import create_merchant_cluster_pair, prediction_layout, \
    prediction_history_table
from frontend.layouts.prediction_layout import estimated_cost
from frontend.layouts.sign_in_layout import sign_in_layout
from frontend.layouts.sign_up_layout import sign_up_layout
from frontend.ui_kit.components.error_message import error_message
from frontend.ui_kit.components.navigation import navigation_bar
from frontend.ui_kit.components.user_balance import user_balance

sign_page_last_click_timestamp = datetime.now()  # to prevent changing page on update


def register_callbacks(_app):
    @_app.callback(
        Output('user-session', 'data'),
        [
            Input('sign-in-session-update', 'data'),
            Input('sign-up-session-update', 'data'),
        ],
        State('user-session', 'data')
    )
    def manage_session(sign_in_data, sign_up_data,
                       current_session):
        ctx = callback_context

        if not ctx.triggered:
            return current_session
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'sign-in-session-update' and sign_in_data:
            return sign_in_data
        elif trigger_id == 'sign-up-session-update' and sign_up_data:
            return sign_up_data

        return current_session

    @_app.callback(
        Output('url', 'pathname'),
        [Input({'type': 'nav-button', 'index': ALL}, 'n_clicks_timestamp'),
         Input('user-session', 'data')],
        State('url', 'pathname'),
        prevent_initial_call=True
    )
    def manage_navigation(n_clicks_timestamp, user_session, pathname):
        global sign_page_last_click_timestamp
        ctx = callback_context

        if user_session and user_session.get('is_authenticated', False) and pathname in ['/sign-in', '/sign-up']:
            return '/prediction'
        else:
            if not ctx.triggered:
                raise PreventUpdate

            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if not button_id:
                raise PreventUpdate

            try:
                button_index = json.loads(button_id.replace('\'', '"'))['index']
            except JSONDecodeError:
                raise PreventUpdate

            click_timestamp = max(n_clicks_timestamp) if n_clicks_timestamp else None

            if click_timestamp and (datetime.now() - sign_page_last_click_timestamp).total_seconds() > 1:
                sign_page_last_click_timestamp = datetime.now()
                if button_index == 'sign-up':
                    return '/sign-up'
                elif button_index == 'sign-in':
                    return '/sign-in'
            else:
                raise PreventUpdate

    @_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')],
        [State('user-session', 'data')]
    )
    def manage_page_content(pathname, user_session):
        if user_session and user_session.get('is_authenticated'):
            if pathname == '/prediction':
                return prediction_layout(user_session)
            elif pathname == '/billing':
                return billing_layout(user_session)
            elif pathname == '/admin':
                if user_session.get('is_superuser'):
                    return admin_layout()
                else:
                    return "403 Access Denied"
            else:
                return "404 Page Not Found"
        else:
            if pathname == '/sign-in':
                return sign_in_layout()
            elif pathname == '/sign-up':
                return sign_up_layout()
            else:
                return dcc.Location(id='url', href='/sign-in', refresh=True)

    @_app.callback(
        Output('nav-bar', 'children'),
        [Input('user-session', 'data')]
    )
    def manage_navigation_bar(user_session):
        if user_session and user_session.get('is_authenticated'):
            return navigation_bar(user_session)
        return ""

    @_app.callback(
        [
            Output('sign-in-session-update', 'data'),
            Output('sign-in-status', 'children'),
        ],
        [
            Input({'type': 'auth-button', 'action': 'sign-in'}, 'n_clicks'),
        ],
        [
            State('user-session', 'data'),
            State('sign-in-email', 'value'),
            State('sign-in-password', 'value'),
        ],
        prevent_initial_call=True
    )
    def sign_in_callback(sign_in_clicks, _, sign_in_email, sign_in_password):
        if sign_in_clicks > 0:
            user_data, error = authenticate_user(sign_in_email, sign_in_password)
            if user_data:
                new_user_session = authentificated_session(user_data)
                return new_user_session, "Sign in successful"
            return None, error_message(error if error else "Invalid credentials")
        raise PreventUpdate

    @_app.callback(
        [
            Output('sign-up-session-update', 'data'),
            Output('sign-up-status', 'children'),
        ],
        [
            Input({'type': 'auth-button', 'action': 'sign-up'}, 'n_clicks'),
        ],
        [
            State('user-session', 'data'),
            State('sign-up-email', 'value'),
            State('sign-up-password', 'value'),
            State('sign-up-name', 'value'),
        ],
        prevent_initial_call=True
    )
    def sign_up_callback(sign_up_clicks, _, sign_up_email, sign_up_password, sign_up_name):
        if sign_up_clicks > 0:
            user_data, error = register_user(sign_up_email, sign_up_password, sign_up_name)
            if user_data:
                new_user_session = authentificated_session(user_data)
                return new_user_session, "Registration successful"

            return {}, error_message(error if error else "Registration failed")

        raise PreventUpdate

    @_app.callback(
        [Output('users-report-div', 'children'),
         Output('predictions-report-div', 'children'),
         Output('credits-report-div', 'children')],
        [Input('refresh-button', 'n_clicks')],
        State('user-session', 'data'),
    )
    def manage_admin_reports(_, user_session):
        try:
            users_report_data = fetch_users_report(user_session=user_session)
            predictions_report_data = fetch_predictions_reports(user_session=user_session)
            credits_report_data = fetch_credits_report(user_session=user_session)
            return (users_report(users_report_data),
                    predictions_report(predictions_report_data),
                    credits_report(credits_report_data))
        except Exception as e:
            return (error_message("Error fetching users report: " + str(e)),
                    error_message("Error fetching predictions report: " + str(e)),
                    error_message("Error fetching credits report: " + str(e)))

    @_app.callback(
        [
            Output('deposit-amount', 'value'),
            Output('transaction-history-table', 'children'),
            Output('current-balance-billing', 'children')
        ],
        [
            Input('deposit-button', 'n_clicks'),
        ],
        [
            State('user-session', 'data'),
            State('deposit-amount', 'value'),
        ]
    )
    def manage_deposit(deposit_clicks, user_session, _deposit_amount):
        if deposit_clicks > 0 and _deposit_amount and _deposit_amount > 0:
            transaction_info = deposit_amount(_deposit_amount, user_session=user_session)

            if transaction_info:
                balance = fetch_user_balance(user_session=user_session)
                transactions = fetch_transaction_history(user_session=user_session)
                return "", transaction_history_table(
                    transactions), user_balance(balance)

        raise PreventUpdate

    @_app.callback(
        [Output('model-dropdown', 'options'),
         Output('model-dropdown', 'value'),
         ],
        Input('model-dropdown', 'options'),
        State('user-session', 'data')
    )
    def manage_models(_, user_session):
        models = fetch_models(user_session)
        dropdown_options = [{'label': model['name'], 'value': model['name']} for model in models]
        return dropdown_options, dropdown_options[0]['value']

    @_app.callback(
        [
            Output('prediction-history-table', 'children'),
            Output('current-balance-predictions', 'children')
        ],
        [
            Input('predict-button', 'n_clicks'),
        ],
        [
            State('user-session', 'data'),
            State('model-dropdown', 'value'),
            State({'type': 'input-merchant', 'index': ALL}, 'value'),
            State({'type': 'input-cluster', 'index': ALL}, 'value'),
        ]
    )
    def manage_predictions(n_clicks, user_session, selected_model, merchant_ids, cluster_ids):
        if n_clicks > 0 and user_session:
            send_prediction_request(selected_model, merchant_ids, cluster_ids, user_session)
            predictions = fetch_prediction_history(user_session=user_session)
            balance = fetch_user_balance(user_session=user_session)
            return prediction_history_table(predictions), user_balance(balance)

        raise PreventUpdate

    @_app.callback(
        Output('merchant-cluster-pairs', 'children'),
        [Input('add-pair-button', 'n_clicks'),
         Input({'type': 'remove-pair', 'index': ALL}, 'n_clicks')],
        [State('merchant-cluster-pairs', 'children')]
    )
    def manage_merchant_pairs(_, __, children):
        def get_index_from_prop_id(prop_id):
            try:
                json_part = prop_id.split('.n_clicks')[0]
                json_part = json_part.replace("'", "\"")
                prop_id_dict = json.loads(json_part)
                return int(prop_id_dict.get("index"))
            except (ValueError, json.JSONDecodeError):
                return None

        ctx = callback_context

        if not ctx.triggered:
            raise PreventUpdate

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'add-pair-button':
            new_index = len(children)
            children.append(create_merchant_cluster_pair(new_index))
            return children

        elif 'remove-pair' in button_id:
            indices_to_remove = [get_index_from_prop_id(trigger['prop_id']) for trigger in ctx.triggered if
                                 'remove-pair' in trigger['prop_id']]
            indices_to_remove = [index for index in indices_to_remove if index is not None]

            if indices_to_remove:
                return [child for i, child in enumerate(children) if i not in indices_to_remove]

        raise PreventUpdate

    @_app.callback(
        Output('estimated-cost', 'children'),
        [Input('model-dropdown', 'value'),
         Input('merchant-cluster-pairs', 'children')],
        [State('user-session', 'data')]
    )
    def update_estimated_cost(selected_model, merchant_pairs, user_session):
        global_models = fetch_models(user_session=user_session)
        if selected_model and merchant_pairs and global_models:
            num_pairs = len(merchant_pairs)
            total_cost = 0

            for model in global_models:
                if model['name'] == selected_model:
                    total_cost = model['cost'] * max(num_pairs, 1)
                    break
            return estimated_cost(total_cost)
        return estimated_cost(None)
