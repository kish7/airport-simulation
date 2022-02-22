import pandas as pd
import pathlib
from datetime import datetime, date, timedelta
import numpy as np
import os.path

FMT = '%H:%M:%S'

def get_processed_data():
    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()
    states = pd.read_csv(DATA_PATH.joinpath("states.csv"))
    states['airline'] = states['callsign'].apply(lambda x: x[:2])
    return states

def get_aircraft_state_time(states):
    path = "visualization-app/data/cache/aircraft_state_time.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    aircraft_state_time = states.sort_values(['callsign', 'time'], ascending=[True, True])
    aircraft_state_time = aircraft_state_time[['callsign', 'state', 'time']]
    aircraft_state_time['prev_state_time'] = aircraft_state_time.time.shift(1)
    aircraft_state_time = aircraft_state_time.reset_index(drop=True)
    aircraft_state_time.to_csv(path, encoding='utf-8')
    return aircraft_state_time

def get_aircraft_stats(states):
    path = "visualization-app/data/cache/aircraft_mins.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    aircraft_mins = pd.DataFrame(columns=('callsign', 'atgate_time', 'pushback_time', 'ramp_time', 'taxi_time', 'stop_time'))
    i = 0
    for callsign in set(states['callsign'].tolist()):
        aircraft_mins.loc[i] = [callsign, get_duration(callsign, 'atGate', states), get_duration(callsign, 'pushback', states), get_duration(callsign, 'ramp', states), get_duration(callsign, 'taxi', states), get_duration(callsign, 'stop', states)]
        i += 1
    aircraft_mins.to_csv(path, encoding='utf-8')
    return aircraft_mins

def get_state_distribution(states):
    path = "visualization-app/data/cache/state_distribution.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    state_distribution = states.sort_values(['time'], ascending=[True])
    state_distribution['hour'] = state_distribution['time'].str[0:2].astype(int)
    state_distribution.to_csv(path, encoding='utf-8')
    return state_distribution

def get_state_distribution_by_hour(state_distribution, states):
    path = "visualization-app/data/cache/state_distribution_by_hour.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    grouped = state_distribution.groupby('hour')['state'].value_counts().groupby(level=0)
    state_distribution_by_hour = pd.DataFrame()
    for name, group in grouped:
        state_distribution_by_hour = state_distribution_by_hour.append(group.unstack(level=1))
    state_distribution_by_hour.to_csv(path, encoding='utf-8')
    return state_distribution_by_hour

def get_duration(callsign, state, states):
    df_state = states.loc[(states['callsign']==callsign) & (states['state']==state)]
    state_time = np.nan
    if len(df_state) != 0:
        state_time = (datetime.strptime(df_state.iloc[-1].time, FMT)-datetime.strptime(df_state.iloc[0].time, FMT)).total_seconds() / 60
    return state_time

def get_state_by_airline(states):
    path = "visualization-app/data/cache/state_by_airline.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    grouped = states.groupby('airline').state.value_counts().groupby(level=0)
    state_by_airline = pd.DataFrame()
    for name, group in grouped:
    #     print(name)
        # print(group.unstack(level=1))
        state_by_airline = state_by_airline.append(group.unstack(level=1))
    state_by_airline.to_csv(path, encoding='utf-8')
    return state_by_airline
