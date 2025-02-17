"""Class file for `StateLogger`."""
import os
import json
import logging

from link import HoldLink
from utils import get_output_dir_name
from datetime import datetime

class StateLogger:
    """`StateLogger` logs the airport states in each tick, parses them into a
    generic file format (JSON) and will be used for visualization. The logs are
    saved to file on the fly; therefore, the logs are still valid even the
    simulation are terminated early.
    """

    def __init__(self):

        self.states = []
        self.idle_aircraft = {}
        self.logger = logging.getLogger(__name__)

        try:
            os.remove(self.output_filename)
        except OSError:
            pass

    def log_on_tick(self, simulation):
        """Logs the simulation states on tick."""

        aircrafts = [
            self.__parse_aircraft(aircraft)
            for aircraft in simulation.airport.aircrafts + simulation.airport.departure_info
        ]

        state = {
            "time": self.__parse_time(simulation.now),
            "aircrafts": aircrafts,
            'takeoff_count': simulation.airport.takeoff_count,
            'total_ticks_on_surface': simulation.airport.takeoff_ticks_count
        }

        with open(self.output_filename, "a") as fout:
            fout.write(json.dumps(state) + "\n")
        return state

    def __parse_aircraft(self, aircraft):

        # check if aircraft is idle
        if aircraft.callsign in self.idle_aircraft:
            if self.idle_aircraft[aircraft.callsign] == aircraft.precise_location.geo_pos:
                aircraft.idle_time = aircraft.idle_time + 1
            else:
                aircraft.idle_time = 0
                del self.idle_aircraft[aircraft.callsign] 
        else:
            self.idle_aircraft[aircraft.callsign] = aircraft.precise_location.geo_pos

        itinerary = self.__parse_itinerary(aircraft.itinerary)
        itinerary_index = aircraft.itinerary.index if itinerary else None

        uc_delayed_index = aircraft.itinerary.uncertainty_delayed_index \
            if itinerary else None
        sc_delayed_index = aircraft.itinerary.scheduler_delayed_index \
            if itinerary else None

        return {
            "callsign": aircraft.callsign,
            "state": aircraft.state.name,
            "speed": aircraft.speed,
            "is_delayed": aircraft.is_delayed,
            "idle_time": aircraft.idle_time,
            "location": aircraft.precise_location.geo_pos,
            "itinerary": itinerary,
            "itinerary_index": itinerary_index,
            "uncertainty_delayed_index": uc_delayed_index,
            "scheduler_delayed_index": sc_delayed_index,
            "takeoff": aircraft.take_off,
            # "estimated_time": aircraft.estimated_time.strftime("%H:%M:%S")
        }

    @classmethod
    def __parse_itinerary(cls, itinerary):
        return [
            {
                "node_name": target.name if type(target) is not HoldLink else None,
                "node_location": target.start.geo_pos if type(target) is not HoldLink else None
            }
            for target in itinerary.targets
        ] if itinerary is not None else None

    @classmethod
    def __parse_time(cls, time):
        return "%02d:%02d:%02d" % (time.hour, time.minute, time.second)

    @property
    def output_filename(self):
        """Gets the output filename of json file storing all the states."""
        return get_output_dir_name() + "states.json"

    def __getstate__(self):
        attrs = dict(self.__dict__)
        del attrs["logger"]
        return attrs

    def __setstate__(self, attrs):
        self.__dict__.update(attrs)
