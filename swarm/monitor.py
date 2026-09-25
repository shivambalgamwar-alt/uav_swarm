class HeartbeatMonitor:
    """
    Tracks how many consecutive heartbeats have been missed for each drone.
    A drone is "declared failed" (from the network's point of view) once
    it misses MISS_THRESHOLD heartbeats in a row — this could mean the
    drone actually crashed, OR it just lost its link (an outage).
    """

    MISS_THRESHOLD = 3

    def __init__(self):
        self.missed_counts = {}     # drone_id -> consecutive misses
        self.declared_failed = set()  # drone_ids currently declared failed

    def update(self, world, graph):
        newly_declared = []
        newly_recovered = []

        for drone in world.drones:
            if not drone.alive:
                # Truly dead — always counts as failed, no need to count misses
                if drone.id not in self.declared_failed:
                    self.declared_failed.add(drone.id)
                    newly_declared.append(drone.id)
                continue

            has_route = drone.id in graph and graph.has_node(drone.id) and \
                        self._has_path_to_gs(graph, drone.id)

            if has_route:
                self.missed_counts[drone.id] = 0
                if drone.id in self.declared_failed:
                    self.declared_failed.discard(drone.id)
                    newly_recovered.append(drone.id)
            else:
                self.missed_counts[drone.id] = self.missed_counts.get(drone.id, 0) + 1
                if self.missed_counts[drone.id] >= self.MISS_THRESHOLD:
                    if drone.id not in self.declared_failed:
                        self.declared_failed.add(drone.id)
                        newly_declared.append(drone.id)

        return newly_declared, newly_recovered

    @staticmethod
    def _has_path_to_gs(graph, drone_id):
        import networkx as nx
        return nx.has_path(graph, drone_id, "GS")