import dash
from flask import Flask
from flask.helpers import get_root_path
from dash import html, dcc


def register_dashapps(app):
    from dashapp.callbacks import register_callbacks
    from dashapp.pages import (
        overview,
        airline
    )

    
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    print(get_root_path(__name__))
    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashapp/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout =  html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
        )
        register_callbacks(dashapp)
