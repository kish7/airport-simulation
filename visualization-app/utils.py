from dash import html
from dash import dcc


def Header(app):
    return html.Div([get_header(app), html.Br([])])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.H5("SFO Flight Visualization V3")],
                        className="seven columns main-title",
                    )
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    html_row = []
    for name in list(df.columns.values):
        html_row.append(html.Td([name]))
    table.append(html.Tr(html_row))

    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
