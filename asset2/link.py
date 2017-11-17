from node import Node
from utils import str2sha1, interpolate_geo

class Link:

    def __init__(self, index, name, nodes):
        if len(nodes) < 2:
            raise Exception("Less than two nodes were given")
        self.index = index
        self.name = name
        self.nodes = nodes
        self.hash = str2sha1("%s#%s#%s" % (self.name, self.index, self.nodes))

    @property
    def length(self):
        length = 0.0
        for i in range(1, len(self.nodes)):
            from_node = self.nodes[i - 1]
            to_node = self.nodes[i]
            length += from_node.get_distance_to(to_node)
        return length

    @property
    def start(self):
        return self.nodes[0]

    @property
    def end(self):
        return self.nodes[len(self.nodes) - 1]

    @property
    def reverse(self):
        """
        Reverses the node orders, which means the start and end are switched.
        """
        return Link(self.index, self.name, self.nodes[::-1])

    def get_node_from_start(self, distance):

        if distance >= self.length:
            # Queried distance is longer than the link
            return self.end

        ratio = distance / self.length
        geo_pos = interpolate_geo(self.start, self.end, ratio)
        return Node(0, "LINK-INTERMEDIATE-POINT", geo_pos)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash

    def __ne__(self, other):
        return not(self == other)

    def __repr__(self):
        return "<Link: " + self.name + ">"
