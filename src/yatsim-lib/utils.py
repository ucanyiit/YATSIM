"""Here are the util functions used in the yatsim library."""

from yatsim.cell import Direction


def move_to_next_cell(x: int, y: int, direction: Direction):
    """Gets the new location when an element moves one step."""
    switch = {0: (x, y - 1), 1: (x + 1, y), 2: (x, y + 1), 3: (x - 1, y)}

    return switch.get(direction.value, "Please give proper input")
