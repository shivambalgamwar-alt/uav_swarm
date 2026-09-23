import math
import networkx as nx

RADIO_RANGE = 40  # metres


def distance(pos_a, pos_b):
    x1, y1 = pos_a
    x2, y2 = pos_b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def build_network_graph(world):
    """Builds a graph of drones + ground station, linked if within RADIO_RANGE."""
    G = nx.Graph()

    # Add ground station as a node
    G.add_node("GS", pos=world.ground_station)

    # Add all alive drones as nodes
    for drone in world.alive_drones():
        G.add_node(drone.id, pos=drone.position())

    # Check every pair of nodes and link if in range
    nodes = list(G.nodes(data="pos"))
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            name_a, pos_a = nodes[i]
            name_b, pos_b = nodes[j]
            d = distance(pos_a, pos_b)
            if d <= RADIO_RANGE:
                G.add_edge(name_a, name_b, dist=d)

    return G


def route_to_ground_station(G, drone_id):
    """Returns the shortest path from drone_id to GS, or None if unreachable."""
    if drone_id not in G or not nx.has_path(G, drone_id, "GS"):
        return None
    return nx.shortest_path(G, drone_id, "GS")