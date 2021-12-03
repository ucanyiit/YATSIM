"""Cell elements of game grid are defined here."""

from typing import List, NewType

# From 0 to 3 N E S W, respectively
Direction = NewType("Direction", int)


class CellElement:
    """Abstract class representing the tiles of the grid.

    Cells have no knowledge of the GameGrid, and therefore do not perform any
    bound checks.

    Attributes:
        orientation: The orientation of the cell.
        x: x component of the coordinates.
        y: y component of the coordinates.
        _entries: List of Directions (ints) for directions with rail entries.
    """

    def __init__(
        self,
        x: int,
        y: int,
    ):
        """Inits CellElement with position, entry directions."""
        self.orientation: Direction = Direction(0)
        self.x = x
        self.y = y
        self._entries: List[Direction] = []

    @property
    def entry_count(self) -> int:
        """The number of directions a direction can enter the cell."""
        return len(self._entries)

    def set_position(self, x: int, y: int) -> None:
        """Sets the coordinates of the cell."""
        self.x = x
        self.y = y

    def rotate(self) -> None:
        """Rotates the cell clockwise."""

        def _mod_incr(x: Direction) -> Direction:
            return Direction((1 + x) % 4)

        self.orientation = _mod_incr(self.orientation)
        for i, entry in enumerate(self._entries):
            self._entries[i] = _mod_incr(entry)

    def set_orientation(self, direction: Direction) -> None:
        """Rotates the cell until the desired direction is achieved."""
        while self.orientation != direction:
            self.rotate()

    # TODO: Discuss this behavior.
    def switch_state(self) -> None:
        """Switches to the next state.

        This method is overriden by stateful subclasses such as railroad switches.
        """
        raise NotImplementedError(self)

    # TODO: implement get_duration.
    def get_duration(self, entdir: Direction) -> float:
        """Returns the duration of the trains passing through the object.

        Precisely, it returns the time interval between train engine entering and
        test leaving the cell.

        Args:
            entdir: The entry direction of the train

        Returns:
            The time the engine spends going through the cell.
        """

    # TODO: fill me.
    def get_stop(self, entdir: Direction) -> float:
        """Returns the amount of time a train engine in this cell."""

    # TODO: fill me.
    def next_cell(self, entdir: Direction) -> "CellElement":
        """Returns the next cell a train will enter based on its entry direction."""

    # TODO: fill me.
    def get_view(self):
        """TODO: fill me."""
