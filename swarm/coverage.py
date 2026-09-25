class CoverageTracker:
    """
    Tracks which parts of the survey area have been visited by dividing
    the whole area into a grid of cells and marking a cell "covered"
    whenever any drone passes close enough to it.
    """

    def __init__(self, width, height, cell_size=5):
        self.cell_size = cell_size
        self.cols = int(width // cell_size) + 1
        self.rows = int(height // cell_size) + 1
        self.covered = [[False] * self.cols for _ in range(self.rows)]

    def update(self, world):
        for drone in world.alive_drones():
            col = int(drone.x // self.cell_size)
            row = int(drone.y // self.cell_size)
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.covered[row][col] = True

    def percent_covered(self):
        total = self.rows * self.cols
        covered = sum(row.count(True) for row in self.covered)
        return 100.0 * covered / total if total else 0.0