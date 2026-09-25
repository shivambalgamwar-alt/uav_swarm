# Resilient UAV Swarm for Disaster-Zone Survey

A Python simulation of a multi-drone swarm that surveys a disaster zone,
relays data back to a ground station through a multi-hop aerial network,
and automatically reconfigures itself when a drone fails or loses
connectivity.

Built for Techfest, IIT Bombay — Stage 1 submission.

## What This Demonstrates

- **BVLOS survey** — drones autonomously fly lawnmower coverage patterns
  over an assigned region, no manual control.
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

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

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

A window will open showing:
- **Blue dots** — healthy drones flying their survey pattern
- **Red dot** — a drone that has crashed (scripted failure at t=15)
- **Orange dot** — a drone that is alive but currently unreachable
  (network outage, not a crash)
- **Green lines** — active radio links between drones/ground station
- **Black square** — the ground station

The console (and `simulation_log.txt`) will print, every step:
- The current multi-hop route from the farthest drone to the ground
  station, or `NO ROUTE (disconnected)` if none exists
- Failure/recovery events from the heartbeat monitor
- Reassignment events when a failed drone's area is redistributed
- Running coverage percentage

The simulation stops automatically after 200 steps and prints a final
summary with total coverage and which drones failed.

## Project Structure
uav-swarm/                      <- your repo root
  main.py                       <- entry point, run this to start the simulation
  requirements.txt
  README.md
  simulation_log.txt            <- generated when you run main.py
  swarm/                        <- your package folder
    __init__.py                 <- empty file, makes it a package
    world.py                    <- Phase 1
    drone.py                    <- Phase 1
    radio.py                    <- Phase 2
    monitor.py                  <- Phase 3
    planner.py                  <- Phase 4
    coverage.py                 <- just added
    logger.py                   <- just added
  explore/
    explore1_simple.py          <- your early learning experiment
    README.md                   <- (or wherever you put the explore1 readme)