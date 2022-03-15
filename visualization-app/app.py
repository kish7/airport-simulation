# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pages import (
    overview,
    airline
)
import logging
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import datetime, date, timedelta
import json
from flask import Flask, render_template, send_from_directory

# app = dash.Dash(
#     __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
# )
# app.title = "Visualization Report"
# server = app.server

server = Flask(__name__)

# # Describe the layout/ UI of the app
# app.layout = html.Div(
#     [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
# )

# # Update page
# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def display_page(pathname):
#     if pathname == "/airline":
#         print("8.1. current time: - ", datetime.now())
#         return airline.create_layout(app)
#     print("8. current time: - ", datetime.now())
#     return overview.create_layout(app)

@server.route('/')
def index():
	return render_template('index.html')

# Get states data
@server.route('/get_states', methods=['GET', 'POST'])
def get_states():
	# f = open('output/real-west-all-terminals/states.json')
    # states = json.load(f)
    states = [json.loads(line) for line in open('output/real-west-all-terminals/states.json', 'r')]
    return json.dumps(states[-1])



    
class OnMyWatch:
    # Set the directory on watch
    # watchDirectory = "/data"
    # TODO change to environment variable
    watchDirectory = r"/Users/suyanxu/NASA/airport-simulation/visualization-app/data"
  
    def __init__(self):
        self.observer = Observer()
  
    def run(self):
        print("Observer started")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
  
        self.observer.join()
  
  
class Handler(FileSystemEventHandler):
  
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
  
        elif event.event_type == 'created':
            print("created file - % s." % event.src_path)
        elif event.event_type == 'modified':
            print("modified file - % s." % event.src_path)
        

if __name__ == "__main__":
    # watch = OnMyWatch()
    # watch.run()
    # app.run_server(debug=True)
    server.run(host="0.0.0.0", port=5002,debug = True)

