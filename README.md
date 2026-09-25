# Resilient UAV Swarm for Disaster-Zone Survey

A Python simulation of a multi-drone swarm that surveys a disaster zone,
relays data back to a ground station through a multi-hop aerial network,
and automatically reconfigures itself when a drone fails or loses
connectivity.

Built for Techfest, IIT Bombay — Stage 1 submission.

## What This Demonstrates

- **BVLOS survey** — drones autonomously fly lawnmower coverage patterns
  over an assigned region, with no manual control.
- **Multi-hop aerial network** — drones relay data to the ground station
  through each other when direct range isn't possible.
- **Failure detection** — a heartbeat/route-monitoring system detects
  when a drone has crashed or lost its link.
- **Swarm reconfiguration** — when a drone fails, its unfinished survey
  area is automatically split and reassigned to the surviving drones.
- **Metrics & logging** — live coverage percentage and a full event log
  written to `simulation_log.txt`.

## Requirements

- Python 3.10+
- See `requirements.txt`

## Installation

\`\`\`bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
\`\`\`

## How to Run

\`\`\`bash
python main.py
\`\`\`

A window will open showing:
- **Blue dots** — healthy drones flying their survey pattern
- **Red dot** — a drone that has crashed (scripted failure, default at t=15)
- **Orange dot** — a drone that is alive but currently unreachable
  (network outage, not a crash)
- **Green lines** — active radio links between drones/ground station
- **Black square** — the ground station

The console (and `simulation_log.txt`) print, every step:
- The current multi-hop route from the farthest drone to the ground
  station, or `NO ROUTE (disconnected)` if none exists
- Failure/recovery events from the heartbeat monitor
- Reassignment events when a failed drone's area is redistributed
- Running coverage percentage

The simulation stops automatically after `MAX_TIME` steps (default 200)
and prints a final summary with total coverage and which drones failed.

## Project Structure

\`\`\`
uav-swarm/
  main.py               # entry point - sets up the world and runs the simulation
  requirements.txt
  README.md
  simulation_log.txt    # generated automatically when main.py runs
  swarm/                # core package
    __init__.py         # empty file, marks this folder as a Python package
    world.py            # 2D environment, ground station, simulation clock
    drone.py            # Drone class: position, movement, alive/failed status
    radio.py            # radio range check, network graph, routing
    monitor.py          # heartbeat-based failure detection
    planner.py          # area partitioning, lawnmower coverage paths, reassignment
    coverage.py         # tracks % of the area actually surveyed
    logger.py           # writes all events to console + simulation_log.txt
  explore/
    explore1_simple.py  # early learning experiment on radio range & multi-hop routing
    README.md           # notes on the explore1 experiment
\`\`\`

## Configuration

Key parameters, adjustable in the relevant files:

| Parameter | File | Meaning |
|---|---|---|
| `RADIO_RANGE` | `swarm/radio.py` | Max distance (m) for two nodes to communicate |
| `MISS_THRESHOLD` | `swarm/monitor.py` | Missed heartbeats before a drone is declared failed |
| `FAILURE_TIME` | `main.py` | Simulation step at which the scripted failure occurs |
| `MAX_TIME` | `main.py` | Total steps before the simulation stops and summarizes |
| `cell_size` | `swarm/coverage.py` | Grid resolution for coverage tracking |

## How the Simulation Maps to Real Hardware

This simulation models the software logic that would run on a Raspberry
Pi companion computer aboard each UAV, communicating with a flight
controller (ArduPilot/PX4) over MAVLink. On real hardware:

- `Drone.step()` would be replaced with MAVLink waypoint commands
  (`pymavlink` / `MAVSDK-Python`).
- The simulated radio range would be replaced by a real mesh network
  (e.g. Wi-Fi ad-hoc with BATMAN-adv) or long-range telemetry radios.
- Heartbeats would be actual MAVLink `HEARTBEAT` messages.
- Position and battery would come from live `GLOBAL_POSITION_INT`
  telemetry instead of simulated coordinates.

Full details are in the accompanying technical proposal.

## Known Limitations (Stage 1 scope)

- 2D simulation only — no terrain or altitude modeling.
- One scripted failure scenario is wired into `main.py`; additional
  scenarios (relay failure, coordinator failure) are described in the
  proposal as planned extensions.
- No physical hardware integration yet — this is a software
  proof-of-concept.

