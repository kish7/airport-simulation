from dash import dcc
from dash import html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd
import pathlib

import numpy as np
import datetime
from datetime import datetime, date, timedelta

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

states = pd.read_csv(DATA_PATH.joinpath("states.csv"))
aircraft_state_time = states.sort_values(['callsign', 'time'], ascending=[True, True])
aircraft_state_time = aircraft_state_time[['callsign', 'state', 'time']]
aircraft_state_time['prev_state_time'] = aircraft_state_time.time.shift(1)
aircraft_state_time = aircraft_state_time.reset_index(drop=True)

def get_duration(callsign, state):
    df_state = states.loc[(states['callsign']==callsign) & (states['state']==state)]
    state_time = np.nan
    if len(df_state) != 0:
        state_time = (datetime.strptime(df_state.iloc[-1].time, FMT)-datetime.strptime(df_state.iloc[0].time, FMT)).total_seconds() / 60
    return state_time
        
aircraft_mins = pd.DataFrame(columns=('callsign', 'atgate_time', 'pushback_time', 'ramp_time', 'taxi_time', 'stop_time'))
FMT = '%H:%M:%S'
i = 0
for callsign in set(states['callsign'].tolist()):
    aircraft_mins.loc[i] = [callsign, get_duration(callsign, 'atGate'), get_duration(callsign, 'pushback'), get_duration(callsign, 'ramp'), get_duration(callsign, 'taxi'), get_duration(callsign, 'stop')]
    i += 1

state_distribution = states.sort_values(['time'], ascending=[True])
state_distribution['hour'] = state_distribution['time'].str[0:2].astype(int)
grouped = state_distribution.groupby('hour')['state'].value_counts().groupby(level=0)
state_distribution_by_hour = pd.DataFrame()
for name, group in grouped:
    state_distribution_by_hour = state_distribution_by_hour.append(group.unstack(level=1))

traffic_load = states.sort_values(['time'], ascending=[True])
traffic_load['hour'] = traffic_load['time'].str[0:2].astype(int)
traffic_grouped = traffic_load.groupby('hour')['callsign'].agg(lambda x: set(x))

aircraft_mins['atgate_time'].mean()
aircraft_mins['pushback_time'].mean()
aircraft_mins['ramp_time'].mean()
aircraft_mins['taxi_time'].mean()
aircraft_mins['stop_time'].mean()
metric = pd.DataFrame(columns=['metric', 'value'])
metric.loc[0] = ['average atGate speed (ft/epoch)', states.loc[states['state']=='atGate']['speed'].mean()]
metric.loc[1] = ['average pushback speed (ft/epoch)', states.loc[states['state']=='pushback']['speed'].mean()]
metric.loc[2] = ['average ramp speed (ft/epoch)', states.loc[states['state']=='ramp']['speed'].mean()]
metric.loc[3] = ['average taxi speed (ft/epoch)', states.loc[states['state']=='taxi']['speed'].mean()]
metric.loc[4] = ['average stop speed (ft/epoch)', states.loc[states['state']=='stop']['speed'].mean()]
metric.loc[5] = ['average atGate time (min)', aircraft_mins['atgate_time'].mean()]
metric.loc[6] = ['average pushback time (min)', aircraft_mins['pushback_time'].mean()]
metric.loc[7] = ['average ramp time (min)', aircraft_mins['ramp_time'].mean()]
metric.loc[8] = ['average taxi time (min)', aircraft_mins['taxi_time'].mean()]
metric.loc[9] = ['average stop time (min)', aircraft_mins['stop_time'].mean()]


def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Daily Summary"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Total Aircraft Number: 356",
                                        style={"color": "#ffffff", "width": "32%", "float": "left", "font-size": "14px"},
                                        className="row",
                                    ),
                                    html.P(
                                        "\
                                    Total Aircraft Number Late at Gate: "+str(len(set(states['callsign'].tolist()))),
                                        style={"color": "#ffffff", "width": "44%", "float": "left", "font-size": "14px"},
                                        className="row",
                                    ),
                                    html.P(
                                        "\
                                    Total Takeoff: 263",
                                        style={"color": "#ffffff", "width": "24%", "float": "left", "font-size": "14px"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Average Metrics"], 
                                        className="subtitle padded",
                                        style={"height": "30px"},
                                    ),
                                    html.Table(make_dash_table(metric)),
                                ],
                                className="six columns",
                                style={"height": "300px", "overflow-x": "scroll", "overflow-y": "scroll"},
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Distribution of States",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=[
                                                        "atGate",
                                                        "pushback",
                                                        "ramp",
                                                        "taxi",
                                                        "stop",
                                                    ],
                                                    y=[
                                                        states['state'].value_counts()['atGate'],
                                                        states['state'].value_counts()['pushback'],
                                                        states['state'].value_counts()['ramp'],
                                                        states['state'].value_counts()['taxi'],
                                                        states['state'].value_counts()['stop'],
                                                    ],
                                                    marker={
                                                        "color": "#2e86c1",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Calibre Index Fund",
                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Distribution of States by Hour",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=list(state_distribution_by_hour.index.values),
                                                    y=list(state_distribution_by_hour['atGate'].values),
                                                    line={"color": "red"},
                                                    mode="lines",
                                                    name="atGate",
                                                ), 
                                                go.Scatter(
                                                    x=list(state_distribution_by_hour.index.values),
                                                    y=list(state_distribution_by_hour['pushback'].values),
                                                    line={"color": "green"},
                                                    mode="lines",
                                                    name="pushback",
                                                ),  
                                                go.Scatter(
                                                    x=list(state_distribution_by_hour.index.values),
                                                    y=list(state_distribution_by_hour['ramp'].values),
                                                    line={"color": "blue"},
                                                    mode="lines",
                                                    name="ramp",
                                                ),  
                                                go.Scatter(
                                                    x=list(state_distribution_by_hour.index.values),
                                                    y=list(state_distribution_by_hour['taxi'].values),
                                                    line={"color": "yellow"},
                                                    mode="lines",
                                                    name="taxi",
                                                ),  
                                                go.Scatter(
                                                    x=list(state_distribution_by_hour.index.values),
                                                    y=list(state_distribution_by_hour['stop'].values),
                                                    line={"color": "black"},
                                                    mode="lines",
                                                    name="stop",
                                                ),  
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                title="",
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                width=340,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0277108433735,
                                                    "y": -0.142606516291,
                                                    "orientation": "h",
                                                },
                                                margin={
                                                    "r": 20,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                xaxis={
                                                    "autorange": True,
                                                    "linecolor": "rgb(0, 0, 0)",
                                                    "linewidth": 1,
                                                    "range": [0, 24],
                                                    "showgrid": False,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                },
                                                yaxis={
                                                    "autorange": False,
                                                    "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                    "mirror": False,
                                                    "nticks": 4,
                                                    "range": [0, 1000],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "ticklen": 10,
                                                    "ticks": "outside",
                                                    "title": "Count",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                    "zerolinewidth": 4,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Traffic Load by Hour",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-3",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=list(traffic_grouped.index.values),
                                                    y=list(map(lambda a : len(a), traffic_grouped.values)),
                                                    line={"color": "blue"},
                                                    mode="lines",
                                                    name="traffic load",
                                                ), 
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                title="",
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                width=340,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0277108433735,
                                                    "y": -0.142606516291,
                                                    "orientation": "h",
                                                },
                                                margin={
                                                    "r": 20,
                                                    "t": 20,
                                                    "b": 20,
                                                    "l": 50,
                                                },
                                                showlegend=True,
                                                xaxis={
                                                    "autorange": True,
                                                    "linecolor": "rgb(0, 0, 0)",
                                                    "linewidth": 1,
                                                    "range": [0, 24],
                                                    "showgrid": False,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                },
                                                yaxis={
                                                    "autorange": False,
                                                    "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                    "mirror": False,
                                                    "nticks": 4,
                                                    "range": [0, 100],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "ticklen": 10,
                                                    "ticks": "outside",
                                                    "title": "Count",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                    "zerolinewidth": 4,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),

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
