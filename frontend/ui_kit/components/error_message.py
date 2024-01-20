from dash import html

from frontend.ui_kit.styles import error_message_style


def error_message(error_text):
    return html.Div(error_text, style=error_message_style)
