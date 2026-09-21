# explore1: Multi-Hop Radio Network Experiment

A small experiment for the UAV swarm project. It shows how drones with a limited radio range form a network, how a far-away drone reaches the ground station through relay drones (multi-hop), and what happens when one drone fails.

## The Idea

Drones talk by radio, and radio only works up to a maximum distance. A drone that is too far from the ground station cannot talk to it directly, so its data must be passed along by other drones, hop by hop.

This script:

1. Places a ground station and three drones on a 2D map.
2. Checks every pair of drones and links the ones within radio range.
3. Finds the multi-hop route from the farthest drone to the ground station.
4. Removes a drone (simulating a failure) and checks whether the network is still connected.

## Requirements

- Python 3.10 or newer
- `networkx`

## Installation

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install networkx
```

## How to Run

```bash
python explore1_simple.py
```

## Configuration

| Setting | Where | Meaning |
|---|---|---|
| `RADIO_RANGE` | top of the script | Maximum distance (metres) at which two drones can talk |
| `drones` | top of the script | Name and (x, y) position of each drone; `GS` is the ground station |

## Example Setup

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

## Expected Output

```
Links: [('GS', 'D1'), ('D1', 'D2'), ('D2', 'D3')]
Route D3 -> GS: ['D3', 'D2', 'D1', 'GS']
Still connected? False
```

- **Route D3 -> GS** shows the multi-hop path: D3 sends through D2, then D1, then reaches the ground station.
- **Still connected? False** is printed after D2 is removed. The chain is broken and D3 is cut off.

## How It Works

1. **Distance:** the distance between two drones is computed with the Pythagorean formula, `sqrt((x2 - x1)^2 + (y2 - y1)^2)`.
2. **Links:** two nested loops visit every pair of drones exactly once. If the distance is at most `RADIO_RANGE`, the pair is recorded as a link.
3. **Graph:** the links are loaded into a `networkx` graph, where drones are nodes and links are edges.
4. **Routing:** `nx.shortest_path` finds the shortest chain of hops between two drones.
5. **Failure:** `G.remove_node("D2")` simulates a UAV failure, and `nx.has_path` checks whether a route still exists.

## Experiments to Try

1. Set `RADIO_RANGE = 80` and see how more links appear and the route gets shorter.
2. Set `RADIO_RANGE = 30` and see how the network breaks apart.
3. Move D3 to `(50, 10)` and see how the links and route change.
4. Add a new drone, for example `"D4": (100, 60)`, and see which drones it connects to.
5. Remove different drones and see which ones break the network.

## Relevance to the Project

| Concept in this script | Project requirement |
|---|---|
| Graph of in-range links | Multi-hop aerial network |
| Route through relay drones | Maintaining communication beyond line of sight |
| Removing a node | Handling UAV failure |
| No path to the ground station | Handling communication outage |

## Next Steps

- Make the drones move over time instead of using fixed positions.
- Detect failures through missed heartbeats instead of deleting a node by hand.
- Move a spare drone into the gap so the network reconnects (reconfiguration).