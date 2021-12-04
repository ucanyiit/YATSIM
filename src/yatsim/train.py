"""Train class is defined here."""

from enum import Enum, auto
from typing import List, Tuple

from yatsim.cell_element import CellElement, Direction


class TrainStatus(Enum):
    """Enumeration representing the state of a train."""

    STOPPED = auto()
    MOVING = auto()
    REVERSE = auto()


class Train:
    """Abstract class representing a train.

    Attributes:
        train_type: The type of a train.
        car_count: y component of the coordinates.
        cell: The cell the main locomotive is currently on.
        status: The current state of the train.
        orientation: The orientation of the train.
            Direction (type alias for int). Can have values from 0 to
            4 for N to W, respectively.
    """

    # Creates a train at given cell with given number of cars behind. The total size of
    # train is ncars+1 including the engine.
    def __init__(self, train_type: int, car_count: int, cell: CellElement) -> None:
        """Inits train with type, number of cars and the initial cell."""
        self.train_type = train_type
        self.car_count = car_count
        self.cell = cell
        self.status: TrainStatus = TrainStatus.STOPPED
        self.orientation = cell.orientation

    def enter_cell(self, cell: CellElement) -> None:
        """Moves the train engine to the given cell."""
        # TODO: Negation can be used here
        self.orientation = Direction((self.cell.next_cell(self.orientation) + 2) % 4)
        self.cell = cell

    def get_status(self) -> TrainStatus:
        """Returns the status of the train (stopped/forwards/backwards)."""
        return self.status

    # TODO: Implement in later phases. (Currently used for pygame)
    def get_geometry(self) -> List[Tuple[int, int, int, int]]:
        """Returns the geometry of the train."""
        cur_cell = self.cell
        # TODO: Commented, because cell.previous(orientation: int) isn't implemented yet
        geometry: List[Tuple[int, int, int, int]] = [
            (cur_cell.x, cur_cell.y, self.train_type, self.orientation)
        ]

        # for _ in range(self.car_count):
        #     prev_cell_orientation = cur_cell.previous(self.orientation)
        #     geometry.append((
        # cur_cell.x, cur_cell.y, self.train_type, prev_cell_orientation))
        #     cur_cell = ???

        return geometry
