from dash import html

from frontend.ui_kit.styles import user_balance_style


def user_balance(_balance):
    return html.H3(f"Balance: {_balance}", style=user_balance_style)
