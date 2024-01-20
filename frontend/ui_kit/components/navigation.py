from dash import dcc, html

from frontend.ui_kit.styles import link_style, navigation_style, navigation_separator_style


def navigation_bar(user_session):
    links = [dcc.Link('Prediction', href='/prediction', style=link_style)]

    if user_session and user_session.get('is_authenticated'):
        links.append(html.Span(' | ', style=navigation_separator_style))
        links.append(dcc.Link('Billing', href='/billing', style=link_style))

        if user_session.get('is_superuser'):
            links.append(html.Span(' | ', style=navigation_separator_style))
            links.append(dcc.Link('Admin', href='/admin', style=link_style))

    return html.Div(links, style=navigation_style)
