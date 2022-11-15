from aircraft import Aircraft
from itinerary import Itinerary
from link import HoldLink
from node import Node

def serialize_target(target):
    data = {
        "name": target.name,
        "nodes": list(map(serialize_node, target.nodes)),
        "segment_lengths": target.segment_lengths, 
        "boundary": target.boundary,
    }
    return data

def serialize_node(node):
    if node is None:
        return {}
    data = {
        "name": node.name,
        "geo_pos": node.geo_pos,
    }
    return data

def serialize_aircraft(aircraft):
    data = {
        "itinerary": {
            "index": aircraft.itinerary.index,
            "targets": list(map(lambda x: serialize_target(x), aircraft.itinerary.targets))
        }
    }
    return data

def deserialize_aircraft(json_map):
    aircraft = Aircraft("F1", "", None, None, None)
    itinerary_info = json_map["itinerary"]
    itinerary = Itinerary()
    itinerary.targets = []
    targets_info = itinerary_info["targets"]
    for target_info in targets_info:
        tmp_target = HoldLink()
        tmp_target.name = target_info["name"]
        tmp_target.nodes = []
        for node_info in target_info["nodes"]:
            if not node_info:
                node = None
            else:
                node = Node(node_info["name"], node_info["geo_pos"])
            tmp_target.nodes.append(node)
        tmp_target.segment_lengths = target_info["segment_lengths"]
        tmp_target.boundary = target_info["boundary"]
        itinerary.targets.append(tmp_target)
    itinerary.index = itinerary_info["index"]

    print(len(itinerary.targets), itinerary.index, itinerary.is_completed)

    aircraft.itinerary = itinerary
    return aircraft
        
    
        



    