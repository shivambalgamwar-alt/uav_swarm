def partition_area(width, height, y_start, y_end, drone_ids):
    """
    Splits the survey area into equal vertical strips, one per drone.
    Returns {drone_id: (x_min, x_max, y_min, y_max)}
    """
    n = len(drone_ids)
    strip_width = width / n
    regions = {}
    for i, drone_id in enumerate(drone_ids):
        x_min = i * strip_width
        x_max = (i + 1) * strip_width
        regions[drone_id] = (x_min, x_max, y_start, y_end)
    return regions


def lawnmower_path(region, spacing=10):
    """
    Generates a back-and-forth (boustrophedon) coverage path
    covering the given (x_min, x_max, y_min, y_max) region.
    """
    x_min, x_max, y_min, y_max = region
    path = []
    y = y_min
    going_right = True
    while y <= y_max:
        if going_right:
            path.append((x_min, y))
            path.append((x_max, y))
        else:
            path.append((x_max, y))
            path.append((x_min, y))
        y += spacing
        going_right = not going_right
    return path


def remaining_region(region, current_x):
    """
    Given a drone's original region and its current x position,
    returns the portion of the strip it had NOT finished yet
    (used to hand off unfinished work when a drone fails).
    """
    x_min, x_max, y_min, y_max = region
    if current_x <= x_min:
        return region  # hasn't really started
    if current_x >= x_max:
        return None  # already finished this strip
    return (current_x, x_max, y_min, y_max)


def split_region_between(region, n):
    """Splits a region into n equal sub-strips (for reassignment)."""
    x_min, x_max, y_min, y_max = region
    width = (x_max - x_min) / n
    return [
        (x_min + i * width, x_min + (i + 1) * width, y_min, y_max)
        for i in range(n)
    ]