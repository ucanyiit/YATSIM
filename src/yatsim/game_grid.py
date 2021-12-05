"""Game grid class is defined in this module."""

from typing import List

from yatsim.cell import CellElement, ImpossiblePathError, SimpleTimedCellFactory
from yatsim.interfaces import OutOfGridException, TrainStatus
from yatsim.train import Train
from yatsim.utils import move_to_next_cell


class GameGrid:
    """Game grid class.

    Attributes:
        height: The height of the grid.
        width: The width of the grid.
        elements: The grid. This is a List of Lists
        that includes all of the cell elements.
        view: The view elements of the whole grid.
    """

    def __init__(self, height: int, width: int) -> None:
        """Init GameGrid with height and width."""
        self._cell_factory = SimpleTimedCellFactory()
        self.height = height
        self.width = width
        self.elements: List[List[CellElement]] = [
            [self._cell_factory.new(x, y, "bg") for x in range(width)]
            for y in range(height)
        ]
        self.update_view()

    def _check_boundries(self, x: int, y: int) -> bool:
        """Checks if the given x and y are in the grid."""
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def add_element(self, cellel: CellElement, x: int, y: int) -> None:
        """Updates the cell with a new one, overwriting the existing one."""
        if self._check_boundries(x, y):
            raise OutOfGridException(
                f"The given x and y should not exceed boundries. X:{x}, Y:{y}"
            )

        self.elements[y][x] = cellel

    # Replace element at the given coordinates with background element
    def remove_element(self, x, y) -> None:
        """Replace the cell with the default cell."""
        if self._check_boundries(x, y):
            raise OutOfGridException(
                f"The given x and y should not exceed boundries. X:{x}, Y:{y}"
            )

        self.elements[y][x] = self._cell_factory.new(x, y, "bg")

    def update_view(self):
        """Updates the view."""
        self.view = [
            [self.elements[i][j].get_view() for j in range(self.width)]
            for i in range(self.height)
        ]

    def display(self) -> List[List[str]]:
        """Displays the current state of the grid."""
        return self.view

    # TODO: Implement simulation in later phases.
    def start_simulation(self):
        """Start the simulation."""

    # TODO: Implement simulation in later phases.
    def set_pause_resume(self):
        """Toggles resume/pause simulation."""

    # TODO: Implement simulation in later phases.
    def stop_simulation(self):
        """Stops the simulation."""


class GameGridWithTrains(GameGrid):
    """Game grid class that includes train data.

    Attributes:
        trains: The train elements in the train.
    """

    def __init__(self, height: int, width: int) -> None:
        """Init GameGrid with height and width."""
        super().__init__(height, width)
        self.trains: List[Train] = []

    def add_train(self, train: Train):
        """Adds a train to the game grid."""
        self.trains.append(train)

    def move_trains(self):
        """Moves trains."""
        # TODO: We should check the reverse train status.
        #   /- - -\
        #  |       |  <- like this.
        #   \- - -/

        for train in self.trains:
            if train.status == TrainStatus.STOPPED:
                continue

            new_x, new_y = move_to_next_cell(
                train.cell.x, train.cell.y, train.orientation
            )

            if self._check_boundries(new_x, new_y):
                train.status = TrainStatus.STOPPED
                continue

            new_cell: CellElement = self.elements[new_y][new_x]
            # Check if we can enter the next cell.
            try:
                _ = new_cell.next_cell(-train.orientation)
                train.enter_cell(new_cell)
            except ImpossiblePathError:
                train.status = TrainStatus.STOPPED
