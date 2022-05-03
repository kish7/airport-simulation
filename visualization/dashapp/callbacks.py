from datetime import datetime as dt
from dash.dependencies import State, Input, Output
import pandas_datareader as pdr

def register_callbacks(dashapp):
    from dashapp.pages import (
        overview,
        airline,
        dynamic
    )

    # Update page
    @dashapp.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/dashboard/airline":
            print("switch to airline ", dt.now())
            return airline.create_layout(dashapp)
        if pathname == "/dashboard/dynamic":
            print("switch to dynamic ", dt.now())
            return dynamic.create_layout(dashapp)
        print("switch to default dashboard", dt.now())
        return overview.create_layout(dashapp)
