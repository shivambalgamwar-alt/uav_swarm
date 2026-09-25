# UAV Swarm

A small UAV swarm project. It explores two ideas:

1. **`explore.py`** – a static experiment that shows how drones with a limited radio range form a network, how a far-away drone reaches the ground station through relay drones (multi-hop), and what happens when one drone fails.
2. **`main.py` + `swarm/`** – a moving simulation where drones fly along waypoint paths inside a bounded world, form radio links as they move, and are animated with matplotlib.

---

## Part 1: Multi-hop Radio Network Experiment (`explore.py`)

The idea: drones talk by radio, and radio only works up to a maximum distance. A drone that is too far from the ground station cannot talk to it directly, so its data must be passed along by other drones, hop by hop.

This script:

1. Places a ground station and three drones on a 2D map.
2. Checks every pair of drones and links the ones within radio range.
3. Finds the multi-hop route from the farthest drone to the ground station.
4. Removes a drone (simulating a failure) and checks whether the network is still connected.

### Example Setup

| Node | Position |
|---|---|
| GS (ground station) | (0, 0) |
| D1 | (30, 10) |
| D2 | (65, 20) |
| D3 | (100, 25) |

With `RADIO_RANGE = 40`, only neighbours in the chain can hear each other:

| Pair | Distance (approx.) | Linked? |
|---|---|---|
| GS - D1 | 31.6 | Yes |
| D1 - D2 | 36.4 | Yes |
| D2 - D3 | 35.4 | Yes |
| GS - D2 | 68 | No |
| D1 - D3 | 71.6 | No |
| GS - D3 | 103 | No |

### Expected Output

```
Route D3 -> GS: ['D3', 'D2', 'D1', 'GS']
Still connected? False
```

- **Route D3 -> GS** shows the multi-hop path: D3 sends through D2, then D1, then reaches the ground station.
- **Still connected? False** is printed after D2 is removed. The chain is broken and D3 is cut off.

### Configuration

| Setting | Where | Meaning |
|---|---|---|
| `RADIO_RANGE` | top of `explore.py` | Maximum distance (metres) at which two drones can talk |
| `drones` | top of `explore.py` | Name and `(x, y)` position of each drone; `GS` is the ground station |

### How It Works

1. **Distance:** the distance between two drones is computed with the Pythagorean formula, `sqrt((x2 - x1)^2 + (y2 - y1)^2)`.
2. **Links:** two nested loops visit every pair of drones exactly once. If the distance is at most `RADIO_RANGE`, the pair is recorded as a link.
3. **Graph:** the links are loaded into a `networkx` graph, where drones are nodes and links are edges.
4. **Routing:** `nx.shortest_path` finds the shortest chain of hops between two drones.
5. **Failure:** `G.remove_node("D2")` simulates a UAV failure, and `nx.has_path` checks whether a route still exists.

### Experiments to Try

1. Set `RADIO_RANGE = 80` and see how more links appear and the route gets shorter.
2. Set `RADIO_RANGE = 30` and see how the network breaks apart.
3. Move D3 to `(50, 10)` and see how the links and route change.
4. Add a new drone, for example `"D4": (100, 60)`, and see which drones it connects to.
5. Remove different drones and see which ones break the network.

---

## Part 2: Moving Swarm Simulation (`main.py` + `swarm/`)

The static experiment turns into a live simulation. Drones are now objects that move along waypoint paths, a `World` keeps track of everything inside a bounded area, and `swarm/radio.py` rebuilds the radio network from live positions every frame — so links form and break as drones fly, and the multi-hop route to the ground station is recomputed each frame.

### Project Structure

```
├── main.py           # sets up the world + drones and runs the animation
├── explore.py        # static multi-hop radio network experiment (Part 1)
└── swarm/
    ├── __init__.py
    ├── drone.py      # the Drone class
    ├── world.py      # the World class
    └── radio.py      # radio-range network graph + routing helpers
```

### The `Drone` class (`swarm/drone.py`)

A single drone. Holds an `(x, y)` position, a speed, a list of waypoints to visit, and an `alive` flag.

| Method | What it does |
|---|---|
| `Drone(id, x, y, speed=2.0)` | Creates a drone at position `(x, y)` |
| `set_path([(x, y), ...])` | Gives the drone a list of waypoints to loop through |
| `step()` | Moves the drone one simulation step toward the next waypoint |
| `position()` | Returns the current position as `(x, y)` |
| `kill()` | Marks the drone as no longer alive |

When a drone closes in on a waypoint it snaps to it and moves to the next one; otherwise it advances a `speed`-sized step in that direction.

### The `World` class (`swarm/world.py`)

The container for the simulation.

| Method | What it does |
|---|---|
| `World(width, height, ground_station=(0, 0))` | Creates a world of the given bounds |
| `add_drone(drone)` | Adds a drone to the world |
| `alive_drones()` | Returns the list of drones that are still alive |
| `step()` | Advances every alive drone one step and increments `world.time` |

### The `radio` module (`swarm/radio.py`)

Brings the Part 1 graph logic into the simulation, using live drone positions.

| Function / constant | What it does |
|---|---|
| `RADIO_RANGE = 40` | Module-level constant: max distance (metres) at which two nodes can talk |
| `distance(pos_a, pos_b)` | Euclidean distance between two `(x, y)` positions |
| `build_network_graph(world)` | Builds a `networkx` graph of the ground station + all alive drones, with an edge wherever a pair is within `RADIO_RANGE` (edge weight = actual distance) |
| `route_to_ground_station(G, drone_id)` | Shortest multi-hop path from `drone_id` to `GS`, or `None` if unreachable |

Dead drones are excluded automatically, because `build_network_graph` only reads `world.alive_drones()`.

### Setting Up a Scenario (`main.py`)

Open `main.py` and change:

| Setting | Where | Meaning |
|---|---|---|
| `World(width, height, ground_station)` | `main.py` | Size of the world and ground station position |
| `Drone("D1", x=..., y=...)` | `main.py` | Drone's name and starting position |
| `d1.set_path([...])` | `main.py` | Waypoints the drone flies through |
| `world.add_drone(d1)` | `main.py` | Registers the drone in the world |
| `RADIO_RANGE` | `swarm/radio.py` | How far apart nodes can be and still be linked |

By default the ground station sits at `(0, 0)` in a 120 × 60 world, three drones fly small loops, and the animation is refreshed every 200 ms.

### How It Works

1. Main creates a `World` and the drones.
2. Each drone gets a path of waypoints and moves one step per frame.
3. Every frame, `world.step()` advances the drones and the scatter plot + labels are refreshed.
4. Every frame, `build_network_graph(world)` rebuilds the radio graph from current positions and draws each link as a green line.
5. Every frame, `route_to_ground_station(G, "D3")` recomputes the multi-hop route and prints it (or `NO ROUTE`) to the console, so you can watch connectivity appear and disappear live.

### Experiments to Try

1. Add more waypoints to a drone's `set_path(...)` to make it fly a different shape.
2. Change `world.step()` usage to run a headless simulation (no matplotlib) by calling it in a loop and printing `drone.position()`.
3. Call `d.kill()` on a drone mid-simulation — it disappears from the graph and the route may break.
4. Add more drones with `world.add_drone(...)` and watch them all move together.
5. Raise `RADIO_RANGE` in `swarm/radio.py` to 80 and watch the network stay connected; drop it to 30 and watch links vanish.

---

## Requirements

- Python 3.10 or newer
- `networkx`
- `numpy`
- `matplotlib`

## Installation

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install networkx numpy matplotlib
```

## How to Run

```bash
# Part 1: static multi-hop experiment
python explore.py

# Part 2: animated swarm simulation
python main.py
```

## Relevance to the Project

| Concept in this repo | Project requirement |
|---|---|
| Graph of in-range links | Multi-hop aerial network |
| Route through relay drones | Maintaining communication beyond line of sight |
| Removing a node / killing a drone | Handling UAV failure |
| No path to the ground station | Handling communication outage |
| Moving drones along paths | Simulating an active flying swarm |
| Links rebuilt from live positions each frame | Network reconfiguration as the swarm moves |

## Next Steps

- Detect failures through missed heartbeats instead of deleting a node by hand.
- Move a spare drone into the gap so the network reconnects (reconfiguration).
- Visualise the route itself (highlight the edges on the current path to GS), not just all links.
- Plot the graph dynamically over time, e.g. log link uptime or route changes.