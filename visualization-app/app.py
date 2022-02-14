# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pages import (
    overview,
    # pricePerformance,
    # portfolioManagement,
    # feesMins,
    # distributions,
    # newsReviews,
)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Visualization Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
