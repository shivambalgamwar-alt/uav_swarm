import matplotlib.pyplot as plt
import matplotlib.animation as animation

from swarm.world import World
from swarm.drone import Drone
from swarm.radio import build_network_graph, route_to_ground_station
from swarm.monitor import HeartbeatMonitor
from swarm.planner import partition_area, lawnmower_path, remaining_region, split_region_between
from swarm.coverage import CoverageTracker      # NEW
from swarm.logger import SimLogger              # NEW

# --- Set up the world ---
world = World(width=120, height=60, ground_station=(0, 0))

d1 = Drone("D1", x=10, y=0)
d2 = Drone("D2", x=50, y=0)
d3 = Drone("D3", x=90, y=0)

world.add_drone(d1)
world.add_drone(d2)
world.add_drone(d3)

regions = partition_area(width=120, height=60, y_start=0, y_end=60,
                          drone_ids=["D1", "D2", "D3"])

for drone in world.drones:
    region = regions[drone.id]
    path = lawnmower_path(region, spacing=15)
    drone.set_path(path)
    drone.region = region

monitor = HeartbeatMonitor()
coverage = CoverageTracker(width=120, height=60, cell_size=5)   # NEW
logger = SimLogger("simulation_log.txt")                        # NEW

FAILURE_TIME = 15
failure_triggered = False
MAX_TIME = 200   # NEW: stop and print summary after this many steps

# --- Visualization ---
fig, ax = plt.subplots()
ax.set_xlim(0, world.width)
ax.set_ylim(0, world.height)
ax.set_title("UAV Swarm - Phase 4: Coverage + Reassignment")

gs_x, gs_y = world.ground_station
ax.plot(gs_x, gs_y, "ks", markersize=10, label="Ground Station")

scat = ax.scatter([], [], c="blue", s=60)
labels = [ax.text(0, 0, d.id, fontsize=8) for d in world.drones]
link_lines = []


def reassign_failed_drone(failed_drone, world):
    leftover = remaining_region(failed_drone.region, failed_drone.x)
    survivors = world.alive_drones()

    if leftover is None or not survivors:
        logger.log(f"[t={world.time}] No leftover area to reassign (or no survivors).")
        return

    sub_regions = split_region_between(leftover, len(survivors))

    for drone, sub_region in zip(survivors, sub_regions):
        extra_path = lawnmower_path(sub_region, spacing=15)
        drone.path.extend(extra_path)
        logger.log(f"[t={world.time}] REASSIGN: {drone.id} takes over region "
                    f"{tuple(round(v, 1) for v in sub_region)}")


def update(frame):
    global link_lines, failure_triggered

    if world.time >= MAX_TIME:
        summary = (f"FINAL COVERAGE: {coverage.percent_covered():.1f}% | "
                    f"Failed drones: {[d.id for d in world.drones if not d.alive]}")
        logger.close(summary)
        ani.event_source.stop()
        return scat, *labels, *link_lines

    world.step()
    coverage.update(world)   # NEW

    if world.time == FAILURE_TIME and not failure_triggered:
        logger.log(f"[t={world.time}] *** SCRIPTED FAILURE: D2 has crashed ***")
        reassign_failed_drone(d2, world)
        d2.kill()
        failure_triggered = True

    positions = []
    colors = []
    for d in world.drones:
        positions.append(d.position())
        if not d.alive:
            colors.append("red")
        elif d.id in monitor.declared_failed:
            colors.append("orange")
        else:
            colors.append("blue")

    scat.set_offsets(positions)
    scat.set_color(colors)

    for label, drone in zip(labels, world.drones):
        label.set_position((drone.x + 1, drone.y + 1))

    for line in link_lines:
        line.remove()
    link_lines = []

    G = build_network_graph(world)
    for a, b in G.edges():
        pos_a = G.nodes[a]["pos"]
        pos_b = G.nodes[b]["pos"]
        line, = ax.plot(
            [pos_a[0], pos_b[0]], [pos_a[1], pos_b[1]],
            "g-", linewidth=1, alpha=0.6
        )
        link_lines.append(line)

    newly_declared, newly_recovered = monitor.update(world, G)
    for drone_id in newly_declared:
        logger.log(f"[t={world.time}] MONITOR: {drone_id} declared FAILED")
    for drone_id in newly_recovered:
        logger.log(f"[t={world.time}] MONITOR: {drone_id} RECOVERED")

    route = route_to_ground_station(G, "D3")
    if route:
        logger.log(f"[t={world.time}] D3 -> GS route: {route} | "
                    f"Coverage: {coverage.percent_covered():.1f}%")
    else:
        logger.log(f"[t={world.time}] D3 -> GS: NO ROUTE (disconnected) | "
                    f"Coverage: {coverage.percent_covered():.1f}%")

    return scat, *labels, *link_lines


ani = animation.FuncAnimation(fig, update, interval=150, cache_frame_data=False)
plt.legend()
plt.show()