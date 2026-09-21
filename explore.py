import networkx as nx
import numpy as np

RADIO_RANGE = 40  # metres
drones = {
    "GS": (0, 0),      # ground station
    "D1": (30, 10),
    "D2": (65, 20),
    "D3": (100, 25),   # far away, only reachable through relays
}

G = nx.Graph()
for name, pos in drones.items():
    G.add_node(name, pos=pos)

names = list(drones)
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        d = np.linalg.norm(np.array(drones[names[i]]) - np.array(drones[names[j]]))
        if d <= RADIO_RANGE:
            G.add_edge(names[i], names[j], dist=d)

print("Route D3 -> GS:", nx.shortest_path(G, "D3", "GS"))

G.remove_node("D2")  # simulate a drone failure
print("Still connected?", nx.has_path(G, "D3", "GS"))

# import math

# RADIO_RANGE = 40

# # name -> (x, y) position
# drones = {
#     "GS": (0, 0),
#     "D1": (30, 10),
#     "D2": (65, 20),
#     "D3": (100, 25),
# }

# def distance(a, b):
#     x1, y1 = a
#     x2, y2 = b
#     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# names = list(drones.keys())   # ["GS", "D1", "D2", "D3"]
# links = []                    # will hold pairs that can talk

# for i in range(len(names)):
#     for j in range(i + 1, len(names)):
#         first = names[i]
#         second = names[j]
#         d = distance(drones[first], drones[second])
#         print(first, "to", second, "=", round(d, 1))
#         if d <= RADIO_RANGE:
#             links.append((first, second))

# print("Links:", links)