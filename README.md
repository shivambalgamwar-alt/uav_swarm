# Resilient UAV Swarm for Disaster-Zone Survey

A Python simulation of a multi-drone swarm that surveys a disaster zone,
relays data back to a ground station through a multi-hop aerial mesh
network, and automatically reconfigures itself when a drone fails or
loses connectivity.

Built for Techfest, IIT Bombay — Stage 1 submission.

## Features

- **BVLOS survey** — drones autonomously fly lawnmower (boustrophedon)
  coverage patterns over their assigned regions, with no manual control.
- **Multi-hop aerial network** — drones relay data to the ground station
  through one another when a direct link is out of range. Routing uses a
  graph built from radio-range links and shortest-path computation.
- **Failure detection** — a heartbeat/route monitor counts consecutive
  missed connections and declares a drone failed (crash *or* link outage)
  after a threshold.
- **Swarm reconfiguration** — when a drone fails, its unfinished survey
  area is split into equal strips and reassigned to the surviving drones,
  which extend their flight paths on the fly.
- **Coverage tracking** — the survey area is divided into a grid; coverage
  percentage is updated live as drones pass over cells.
- **Heatbeat recovery** — drones that lose their link but are still alive
  are flagged "recovered" automatically once a route to the ground station
  is re-established.
- **Metrics & logging** — live coverage percentage and a full event log
  written to `simulation_log.txt`.

## Requirements

- Python 3.10+
- See `requirements.txt` (matplotlib, networkx, numpy)

## Installation

```bash
git clone https://github.com/shivambalgamwar-alt/uav_swarm.git
cd uav_swarm

python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

An animated window will open showing:

- **Blue dots** — healthy drones flying their survey pattern
- **Red dot** — a drone that has crashed (scripted failure, default at t=15)
- **Orange dot** — a drone that is alive but currently unreachable
  (network outage, not a crash)
- **Green lines** — active radio links between drones / ground station
- **Black square** — the ground station

The console (and `simulation_log.txt`) print, every step:

- The current multi-hop route from the farthest drone (`D3`) to the ground
  station, or `NO ROUTE (disconnected)` if none exists
- Failure/recovery events from the heartbeat monitor
- Reassignment events when a failed drone's area is redistributed
- Running coverage percentage

The simulation stops automatically after `MAX_TIME` steps (default 200)
and the log closes with a final summary: total coverage and which drones
failed.

## Project Structure

```
uav-swarm/
  main.py               # entry point — sets up the world and runs the simulation
  explore.py            # standalone experiment on radio range & multi-hop routing
  requirements.txt
  README.md
  simulation_log.txt    # generated automatically when main.py runs
  swarm/                # core package
    __init__.py         # empty file, marks this folder as a Python package
    world.py            # 2D environment, ground station, simulation clock
    drone.py            # Drone class: position, movement, alive/failed status
    radio.py            # radio range check, network graph, shortest-path routing
    monitor.py          # heartbeat-based failure/recovery detection
    planner.py          # area partitioning, lawnmower paths, failure reassignment
    coverage.py         # grid-based tracking of the % of the area surveyed
    logger.py           # writes all events to console + simulation_log.txt
```

## Configuration

Key parameters, adjustable in the relevant files:

| Parameter | File | Meaning |
|---|---|---|
| `RADIO_RANGE` | `swarm/radio.py` | Max distance (m) for two nodes to communicate |
| `MISS_THRESHOLD` | `swarm/monitor.py` | Missed heartbeats before a drone is declared failed |
| `FAILURE_TIME` | `main.py` | Simulation step at which the scripted failure occurs |
| `MAX_TIME` | `main.py` | Total steps before the simulation stops and summarizes |
| `cell_size` | `swarm/coverage.py` | Grid resolution for coverage tracking |
| `spacing` | `swarm/planner.py` | Row spacing of the lawnmower coverage path |

## How the Simulation Maps to Real Hardware

This simulation models the software logic that would run on a Raspberry Pi
companion computer aboard each UAV, communicating with a flight controller
(ArduPilot / PX4) over MAVLink. On real hardware:

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