from dash import dcc
from dash import html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib

import numpy as np
import datetime
from datetime import datetime, date, timedelta
from pages.process import get_processed_data, get_aircraft_stats, get_aircraft_state_time, get_state_distribution, get_state_distribution_by_hour

print("1.1. current time: - ", datetime.now())
states = get_processed_data()

print("2.1. current time: - ", datetime.now())
aircraft_state_time = get_aircraft_state_time(states)

print("3.1. current time: - ", datetime.now())
aircraft_mins = get_aircraft_stats(states)

print("4.1. current time: - ", datetime.now())
state_distribution = get_state_distribution(states)

print("5.1. current time: - ", datetime.now())
state_distribution_by_hour = get_state_distribution_by_hour(state_distribution, states)

print("6.1. current time: - ", datetime.now())
traffic_load = states.sort_values(['time'], ascending=[True])
traffic_load['hour'] = traffic_load['time'].str[0:2].astype(int)
traffic_grouped = traffic_load.groupby('hour')['callsign'].agg(lambda x: set(x))

print("7.1. current time: - ", datetime.now())
def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # 
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Duration by Callsign"], 
                                        className="subtitle padded",
                                        style={"height": "30px"},
                                    ),
                                    html.Table(make_dash_table(aircraft_mins)),
                                ],
                                className="six columns",
                                style={"height": "400px", "overflow-x": "scroll", "overflow-y": "scroll"},
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["Aircraft state time"],
                                        className="subtitle padded",
                                        style={"height": "30px"},
                                    ),
                                    html.Table(make_dash_table(aircraft_state_time)),
                                ],
                                className="six columns",
                                style={"height": "400px", "overflow-x": "scroll", "overflow-y": "scroll"},
                            ),
                        ],
                        className="row ",
                    )
                    # 
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
