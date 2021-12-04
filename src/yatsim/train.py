"""Train class is defined here."""

from enum import Enum, auto

from yatsim.cell_element import CellElement


class TrainStatus(Enum):
    """Enumeration representing the state of a train."""

    STOPPED = auto
    MOVING = auto
    REVERSE = auto


class Train:
    """The train class."""

    # TODO: what does type do?
    # Creates a train at given cell with given number of cars behind. The total size of
    # train is ncars+1 including the engine.
    def __init__(self, train_type, car_count: int, cell: CellElement) -> None:
        """Inits train with type, number of cars and the initial cell."""
        self.train_type = train_type
        self.ncars = car_count
        self.cell = cell
        self.status: TrainStatus = TrainStatus.STOPPED

    # TODO: Implement Train.enter_cell.
    def enter_cell(self, cell: CellElement) -> None:
        """Moves the train engine to the given cell."""

    def get_status(self) -> TrainStatus:
        """Returns the status of the train (stopped/forwards/backwards)."""
        return self.status

    # TODO: Implement Train.get_geometry IN LATER PHASES.
    def get_geometry(self):
        """Returns the geometry of the train."""
