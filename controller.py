"""
Ground Controller oversees the aircraft movement on the ground. It continuously observes the world and sends
commands to pilots when there is a notable situation.
"""
import collections
from json import loads
from kafka import KafkaConsumer

from config import Config

from json_serializer import *

class Controller:
    def __init__(self, ground=None):
        self.ground = ground

        self.PILOT_VISION = Config.params["aircraft_model"]["pilot_vision"]
        self.CLOSE_NODE_THRESHOLD = Config.params["simulation"]["close_node_threshold"]

        self.fake_ground = {}

    def tick(self):
        self.__observe()
        self.__resolve_conflicts()

    def __observe(self):
        aircraft_list = self.ground.aircrafts if self.ground else self.fake_ground["aircrafts"]

        self.aircraft_location_lookup = collections.defaultdict(list)  # {link: (aircraft, distance_on_link)}
        self.aircraft_ahead_lookup = {}  # {aircraft: (target_speed, relative_distance)}

        self.conflicts = []

        """
        Observe the invertedAircraftLocations = {link: (aircraft, distance_on_link)} set.
        Observe the closestAircraft = {aircraft: (target_speed, relative_distance)} dict.
        Observe potential conflicts.
        """
        for aircraft in aircraft_list:
            if aircraft.itinerary.is_completed:
                continue
            link, distance = aircraft.itinerary.current_target, aircraft.itinerary.current_distance
            self.aircraft_location_lookup[link].append((aircraft, distance))

        # Sort the {link: (aircraft, distance_on_link)} by distance_on_link.
        for _, aircraft_pair in self.aircraft_location_lookup.items():
            aircraft_pair.sort(key=lambda pair: pair[1])

        for aircraft in aircraft_list:
            if aircraft.itinerary.is_completed:
                continue
            try:
                target_speed, relative_distance, fronter_aircraft = self.__find_aircraft_ahead(aircraft)
                self.aircraft_ahead_lookup[aircraft] = (target_speed, relative_distance)
                # TODO: discuss with zy & what if none
                aircraft.set_fronter_info((target_speed, relative_distance))
                aircraft.set_fronter_aircraft(fronter_aircraft)
            except NoCloseAircraftFoundError:
                # TODO: discuss with zy & what if none
                aircraft.set_fronter_info(None)
                # TODO: currently just assume the front is moving
                # aircraft.set_fronter_info((200, 100))
                pass

    def __find_aircraft_ahead(self, aircraft):
        link_index, link_distance = aircraft.itinerary.current_target_index, aircraft.itinerary.current_distance

        relative_distance = -link_distance
        for index in range(link_index, aircraft.itinerary.length):
            link = aircraft.itinerary.targets[index]

            aircraft_on_same_link = self.aircraft_location_lookup.get(link, [])
            rear_aircraft, rear_dist = None, -1
            for item in aircraft_on_same_link:
                item_aircraft, item_distance = item
                # Skip if the item is behind the aircraft
                if index == link_index and item_distance <= link_distance:
                    continue

                # Found an aircraft ahead!
                relative_distance += item_distance

                if relative_distance < self.CLOSE_NODE_THRESHOLD:
                    self.conflicts.append((aircraft, item_aircraft))

                if relative_distance > self.PILOT_VISION:
                    continue
                if rear_aircraft is None:
                    rear_aircraft, rear_dist = item_aircraft, relative_distance
                elif relative_distance < rear_dist:
                    rear_aircraft, rear_dist = item_aircraft, relative_distance
            if rear_aircraft is not None:
                return rear_aircraft.speed, rear_dist, rear_aircraft

            relative_distance += link.length

        raise NoCloseAircraftFoundError

    # def __find_aircraft_ahead(self, aircraft):
    #     link_index, link_distance = aircraft.itinerary.current_target_index, aircraft.itinerary.current_distance

    #     link = aircraft.itinerary.targets[link_index]
    #     aircraft_on_same_link = self.aircraft_location_lookup.get(link, [])
    #     relative_distance = -link_distance
    #     for item in aircraft_on_same_link:
    #         item_aircraft, item_distance = item
    #         # Skip if the item is behind the aircraft
    #         if item_distance <= link_distance:
    #             continue
    #         # Found an aircraft ahead!
    #         relative_distance += item_distance
    #         if relative_distance <= self.PILOT_VISION:
    #             return item_aircraft.speed, relative_distance, item_aircraft

    #     for index in range(link_index + 1, aircraft.itinerary.length):
    #         link = aircraft.itinerary.targets[index]
    #         aircraft_on_same_link = self.aircraft_location_lookup.get(link, [])
    #         rear_aircraft, rear_dist = None, -1
    #         for item in aircraft_on_same_link:
    #             item_aircraft, item_distance = item
    #             if rear_aircraft is None:
    #                 rear_aircraft, rear_dist = item_aircraft, item_distance
    #                 continue
    #             if item_distance < rear_dist:
    #                 rear_aircraft, rear_dist = item_aircraft, item_distance
    #         if rear_aircraft is not None:
    #             return rear_aircraft.speed, rear_dist, rear_aircraft
    #     raise NoCloseAircraftFoundError


    #     relative_distance = -link_distance
    #     for index in range(link_index, aircraft.itinerary.length):
    #         link = aircraft.itinerary.targets[index]

    #         aircraft_on_same_link = self.aircraft_location_lookup.get(link, [])
    #         for item in aircraft_on_same_link:
    #             item_aircraft, item_distance = item
    #             # Skip if the item is behind the aircraft
    #             if index == link_index and item_distance <= link_distance:
    #                 continue

    #             # Found an aircraft ahead!
    #             relative_distance += item_distance

    #             if relative_distance < self.CLOSE_NODE_THRESHOLD:
    #                 self.conflicts.append((aircraft, item_aircraft))

    #             if relative_distance > self.PILOT_VISION:
    #                 # Too far that the pilot can't see the aircraft
    #                 raise NoCloseAircraftFoundError
    #             else:
    #                 return item_aircraft.speed, relative_distance, item_aircraft

    #         relative_distance += link.length

    #     raise NoCloseAircraftFoundError

    def __resolve_conflicts(self):
        """
        If two aircraft on two links would enter the same link using their current speed, we see a potential conflict.
        Send command to one of the pilots to wait there.
        Will call Aircraft.Pilot.Slowdown() or something alike.
        """
        priority_list = self.ground.priority if self.ground else self.fake_ground["priority"]

        # TODO: compare the departure time and pioritize the one with longer delay 
        for aircraft_1, aircraft_2 in self.conflicts:
            aircraft_2.set_fronter_info((-1, -1))

    def get_closest_aircraft_ahead(self, aircraft):
        return self.aircraft_ahead_lookup.get(aircraft, None)


class NoCloseAircraftFoundError(Exception):
    pass


if __name__ == "__main__":
    print("controller started")
    controller = Controller()
    consumer = KafkaConsumer(
        'controller',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for message in consumer:
        message = message.value
        controller.fake_ground["priority"] = message["priority"]
        controller.fake_ground["aircrafts"] = list(map(deserialize_aircraft, message["aircrafts"]))
        controller.tick()