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
import logging
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

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
    watch = OnMyWatch()
    watch.run()
    app.run_server(debug=True)

