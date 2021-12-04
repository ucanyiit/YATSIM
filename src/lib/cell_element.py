"""Cell elements of game grid are defined here."""

from typing import Dict, NewType

# From 0 to 3 N E S W, respectively.
Direction = NewType("Direction", int)


# TODO: ~~discuss~~ implement _entries.
class CellElement:
    """Abstract class representing the tiles of the grid.

    Cells have no knowledge of the GameGrid, and therefore do not perform any
    bound checks.

    Attributes:
        orientation: The orientation of the cell.
        x: x component of the coordinates.
        y: y component of the coordinates.
        _orientation:
            Direction (type alias for int). Can have values from 0 to
            4 for N to W, respectively.
        _paths: Dict of Direction to Direction.
        _entries: TODO
    """

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        """Inits CellElement with position, entry directions."""
        self.orientation: Direction = Direction(0)
        self.x = x
        self.y = y
        self._paths: Dict[Direction, Direction] = {}

    def set_position(self, x: int, y: int) -> None:
        """Sets the coordinates of the cell."""
        self.x = x
        self.y = y

    def rotate(self, n: int) -> None:
        """Rotates the cell clockwise.

        Rotates the cell clockwise n-many times.

        """

        def _mod_incr(x: Direction) -> Direction:
            return Direction((n + x) % 4)

        self.orientation = _mod_incr(self.orientation)
        new_paths: Dict[Direction, Direction] = {}
        for k, v in self._paths.items():
            new_paths[_mod_incr(k)] = _mod_incr(v)
        self._paths = new_paths

    def set_orientation(self, direction: Direction) -> None:
        """Rotates the cell until the desired direction is achieved."""
        diff = direction - self.orientation
        diff += 4 if diff < 0 else 0
        self.rotate(diff)

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

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the next cell a train will enter based on its entry direction."""
        return self._paths[entdir]

    # TODO: fill me.
    def get_view(self) -> str:
        """TODO: fill me."""


class BackgroundCellElement(CellElement):
    """TODO."""

    # TODO: BG cell

    def switch_state(self) -> None:
        """Does nothing."""
        pass


class StatefulCell(CellElement):
    """Abstract subclass of CellElement with stateful behavior."""

    def __init__(self, x: int, y: int):
        """Inits the stateful cell with the default state (0)."""
        super().__init__(x, y)
        self._state: int = 0


class SimpleCellElement(StatefulCell):
    """TODO."""

    # TODO: Implement me
    pass


# TODO: Think of a nice way for 3- and more- way cells with junctions etc.
# class TwoWayJunctionRight(CellElement):
#     def __init__(self, x:int, y:int):
#         super().__init__(x, y)
#         self._state: int = 0
#         self._state_count : int = 2
#         self._paths = {} * self._state_count
#         self._paths1 = {}
#         self._paths[Direction(0)] = Direction(2)
#         self._paths[Direction(1)] = Direction(2)
#         self._paths[Direction(2)] = Direction(0)
#         self._paths[Direction(0)] = Direction(2)
#         self._paths[Direction(1)] = Direction(2)
#         self._paths[Direction(2)] = Direction(0)
#     def switch_state(self):
#         pass
