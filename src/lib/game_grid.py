"""Game grid class is defined in this module."""

from typing import Any, List

from lib.cell_element import CellElement


# TODO: Discuss cell factory, view visitor, observers, undo-redo.
class GameGrid:
    """Game grid class."""

    def __init__(self, height: int, width: int) -> None:
        """Init GameGrid with height and width."""
        self.height = height
        self.width = width
        self.elements: List[CellElement] = []
        self.view: List[Any]

        # TODO: views and elements.
        # self.elements = [
        #     [BackgroundCellElement for _ in range(width)] for _ in range(height)
        # ]
        # self.view = [
        #     [
        #         self.elements[i][j].getView() for j in range(width)
        #     ] for i in range(height)
        # ]

    # TODO: Discuss out of boundaries
    def add_element(self, cellel: CellElement, x: int, y: int) -> None:
        """Updates the cell with a new one, overwriting the existing one."""

    # TODO: Discuss out of boundaries, what if the cell is already bg?
    # Replace element at the given coordinates with background element
    def remove_element(self, x, y) -> None:
        """Replace the cell with the default cell."""

    # TODO: Discuss the views.
    # Call when the model is changed so the views are informed
    def update_view(self):
        """Updates the view."""
        self.view = [
            [self.elements[i][j].getView() for j in range(self.width)]
            for i in range(self.height)
        ]

    # TODO: gui display

    # TODO: Discuss display method.
    def display(self) -> str:
        """Displays the current state of the grid."""
        lines = ["".join(self.view[i]) for i in range(self.height)]
        return "\n".join(lines)

    # TODO: Implement simulation
    def start_simulation(self):
        """Start the simulation."""

    # TODO: Implement simulation
    def set_pause_resume(self):
        """Toggles resume/pause simulation."""

    # TODO: Implement simulation
    def stop_simulation(self):
        """Stops the simulation."""
