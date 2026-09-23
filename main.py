import matplotlib.pyplot as plt
import matplotlib.animation as animation

from swarm.world import World
from swarm.drone import Drone

# --- Set up the world ---
world = World(width=120, height=60, ground_station=(0, 0))

d1 = Drone("D1", x=10, y=10)
d1.set_path([(30, 10), (30, 40), (10, 40), (10, 10)])  # simple loop

d2 = Drone("D2", x=60, y=20)
d2.set_path([(80, 20), (80, 45), (60, 45), (60, 20)])

d3 = Drone("D3", x=100, y=25)
d3.set_path([(110, 25), (110, 50), (100, 50), (100, 25)])

world.add_drone(d1)
world.add_drone(d2)
world.add_drone(d3)

# --- Visualization ---
fig, ax = plt.subplots()
ax.set_xlim(0, world.width)
ax.set_ylim(0, world.height)
ax.set_title("UAV Swarm - Phase 1")

gs_x, gs_y = world.ground_station
ax.plot(gs_x, gs_y, "ks", markersize=10, label="Ground Station")

scat = ax.scatter([], [], c="blue", s=60)
labels = [ax.text(0, 0, d.id, fontsize=8) for d in world.drones]

def update(frame):
    world.step()
    positions = [d.position() for d in world.alive_drones()]
    if positions:
        scat.set_offsets(positions)
    for label, drone in zip(labels, world.drones):
        label.set_position((drone.x + 1, drone.y + 1))
    return scat, *labels

ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.legend()
plt.show()