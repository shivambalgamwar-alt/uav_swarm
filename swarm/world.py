class World:
    def __init__(self, width, height, ground_station=(0, 0)):
        self.width = width
        self.height = height
        self.ground_station = ground_station
        self.drones = []
        self.time = 0

    def add_drone(self, drone):
        self.drones.append(drone)

    def alive_drones(self):
        return [d for d in self.drones if d.alive]

    def step(self):
        for drone in self.alive_drones():
            drone.step()
        self.time += 1