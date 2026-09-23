import math

class Drone:
    def __init__(self, drone_id, x, y, speed=2.0):
        self.id = drone_id
        self.x = x
        self.y = y
        self.speed = speed
        self.alive = True
        self.path = []       # list of (x, y) waypoints to visit
        self.path_index = 0

    def set_path(self, path):
        self.path = path
        self.path_index = 0

    def step(self):
        """Move one simulation step toward the next waypoint."""
        if not self.alive or not self.path:
            return
        if self.path_index >= len(self.path):
            return  # reached the end of its path

        target_x, target_y = self.path[self.path_index]
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist < self.speed:
            # close enough, snap to the waypoint and move to the next one
            self.x, self.y = target_x, target_y
            self.path_index += 1
        else:
            # move a "speed"-sized step toward the target
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def position(self):
        return (self.x, self.y)

    def kill(self):
        self.alive = False