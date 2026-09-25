import datetime

class SimLogger:
    """Writes every event to both the console and a log file."""

    def __init__(self, filepath="simulation_log.txt"):
        self.file = open(filepath, "w", encoding="utf-8")
        self.log(f"=== Simulation started {datetime.datetime.now()} ===")

    def log(self, message):
        print(message)
        self.file.write(message + "\n")
        self.file.flush()

    def close(self, summary=None):
        if summary:
            self.log(summary)
        self.log(f"=== Simulation ended {datetime.datetime.now()} ===")
        self.file.close()