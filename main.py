import matplotlib.pyplot as plt
import matplotlib.animation as animation

from swarm.world import World
from swarm.drone import Drone
from swarm.radio import build_network_graph, route_to_ground_station

# --- Set up the world ---
world = World(width=120, height=60, ground_station=(0, 0))

d1 = Drone("D1", x=10, y=10)
d1.set_path([(30, 10), (30, 40), (10, 40), (10, 10), (30, 10)])

d2 = Drone("D2", x=60, y=20)
d2.set_path([(80, 20), (80, 45), (60, 45), (60, 20), (80, 20)])

d3 = Drone("D3", x=100, y=25)
d3.set_path([(110, 25), (110, 50), (100, 50), (100, 25), (110, 25)])

world.add_drone(d1)
world.add_drone(d2)
world.add_drone(d3)

# --- Visualization ---
fig, ax = plt.subplots()
ax.set_xlim(0, world.width)
ax.set_ylim(0, world.height)
ax.set_title("UAV Swarm - Phase 2: Network Links")

gs_x, gs_y = world.ground_station
ax.plot(gs_x, gs_y, "ks", markersize=10, label="Ground Station")

scat = ax.scatter([], [], c="blue", s=60)
labels = [ax.text(0, 0, d.id, fontsize=8) for d in world.drones]

# Lines for network links; recreated each frame
link_lines = []


def update(frame):
    global link_lines

    world.step()

    positions = [d.position() for d in world.alive_drones()]
    if positions:
        scat.set_offsets(positions)
    for label, drone in zip(labels, world.drones):
        label.set_position((drone.x + 1, drone.y + 1))

    # Remove old link lines from the plot
    for line in link_lines:
        line.remove()
    link_lines = []

    # Build the current network graph and draw links
    G = build_network_graph(world)
    for a, b in G.edges():
        pos_a = G.nodes[a]["pos"]
        pos_b = G.nodes[b]["pos"]
        line, = ax.plot(
            [pos_a[0], pos_b[0]], [pos_a[1], pos_b[1]],
            "g-", linewidth=1, alpha=0.6
        )
        link_lines.append(line)

    # Print the route from the farthest drone (D3) to the ground station
    route = route_to_ground_station(G, "D3")
    if route:
        print(f"[t={world.time}] D3 -> GS route: {route}")
    else:
        print(f"[t={world.time}] D3 -> GS: NO ROUTE (disconnected)")

    return scat, *labels, *link_lines


ani = animation.FuncAnimation(fig, update, interval=200, cache_frame_data=False)
plt.legend()
plt.show()