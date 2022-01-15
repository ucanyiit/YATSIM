"""Cell elements of game grid are defined here."""

# Direction        o -- >
# Orientation < -- o --->

from enum import Enum
from typing import Literal, Tuple

# From 0 to 3 N E S W, respectively.
# Direction = NewType("Direction", int)


class ImpossiblePathError(Exception):
    """Raised when next_cell method is erronously called.

    Possible erronous calls are calling the method for an unsuitable subclass or for a
    suitable class with wrong arguments e.g. cell has no entry from this side.
    """


class Direction(Enum):
    """Enumeration covering four directions. They have values from 0 to 3."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __add__(self, value: int) -> "Direction":
        """Implements self + value."""
        return Direction((self.value + value) % 4)

    def __neg__(self) -> "Direction":
        """Implements -self."""
        return Direction(self + 2)


class CellElement:
    """Abstract class representing the tiles of the grid.

    Cells have no knowledge of the GameGrid, and therefore do not perform any
    bound checks.

    Attributes:
        direction: The direction of the cell.
        x: x component of the coordinates.
        y: y component of the coordinates.
        direction:
            An enumeration value. Can have values from 0 to
            4 for N to W, respectively.
    """

    _view: int

    def __init__(
        self,
        x: int,
        y: int,
    ) -> None:
        """Inits CellElement with position, entry directions."""
        self.direction = Direction.NORTH
        self.x = x
        self.y = y

    def set_position(self, x: int, y: int) -> None:
        """Sets the coordinates of the cell."""
        self.x = x
        self.y = y

    def set_direction(self, direction: Direction) -> None:
        """Sets the direction of the cell.

        Can be extended by subclasses if required.
        """
        self.direction = direction

    def switch_state(self) -> None:
        """Switches to the next state.

        By default, it does nothing. This method is overriden by stateful subclasses
        such as railroad switches.
        """

    def get_duration(self, entdir: Direction) -> float:
        """Returns the duration of the trains passing through the object."""
        raise NotImplementedError()

    def get_stop(self, entdir: Direction) -> float:
        """Returns the amount of time a train engine in this cell."""
        raise NotImplementedError()

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the next cell a train will enter based on its entry direction."""
        raise NotImplementedError()

    def get_view(self) -> Tuple[int, int]:
        """Returns the URI for displaying the cell."""
        return self._view, self.direction.value


class SimpleTimedCellElement(CellElement):
    """Implements get_duration and get_stop methods with constants.

    get_duration and get_stop returns 5.0 and 0.0, respectively by default.
    This behavior can be changed by supplying these values in init.

    See superclass CellElement.

    Attributes:
        _total_duration: The amount of time a train spends in this cell.
        _stop_duration: The amount of time a train will be still in this cell.
    """

    def __init__(
        self, x: int, y: int, total_duration: float = 5.0, stop_duration: float = 0.0
    ) -> None:
        """Inits the cell with total and stop duration info.

        Extends CellElement.__init__. By default, total duration is 5 and stop
        duration is 0.
        """
        super().__init__(x, y)
        self._total_duration = total_duration
        self._stop_duration = stop_duration

    def get_duration(self, _entdir: Direction) -> float:
        """Returns the total duration a train will spend in this cell.

        Entry direction is ignored.
        """
        return self._total_duration

    def get_stop(self, _entdir: Direction) -> float:
        """Returns the duration a train will be still in this cell.

        Entry direction is ignored.
        """
        return self._stop_duration


class SimpleTimedBackgroundCellElement(SimpleTimedCellElement):
    """Background cell. Trains can not pass through this cell."""

    _view = 0

    def next_cell(self, _entdir: Direction) -> Direction:
        """Raises ImpossiblePathError."""
        raise ImpossiblePathError("Background cells can not have successor cells.")


class SimpleTimedStraightCellElement(SimpleTimedCellElement):
    """Straight cell with a path oriented vertically upon init."""

    _view = 1

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the next cell the train will visit.

        Returns the opposite direction if entry and the path have the same orientation.
        Otherwise raises ImpossiblePathError.
        """
        if (entdir.value % 2) == (self.direction.value % 2):
            return -entdir
        raise ImpossiblePathError(f"Can not enter cell from {entdir}.")


class SimpleTimedStation(SimpleTimedStraightCellElement):
    """Straight cell with station view. Currently has no additional functionality."""

    _view = 8


class SimpleTimedCurvedCellElement(SimpleTimedCellElement):
    """Curved cell with a path from NORTH to EAST.

    Rotate the cell for achieving different paths.
    """

    _view = 2

    def next_cell(self, entdir: Direction) -> Direction:
        """Return the next cell the train will visit.

        The path goes from the direction the cell faces to, to the 90 degree cw of the
        cell. For example, if the cell is facing EAST, there is a path between EAST and
        NORTH.

        If the entry direction is outside these directions, ImpossiblePathError is
        raised.
        """
        if entdir == self.direction:
            return self.direction + 1
        if entdir == self.direction + 1:
            return self.direction
        raise ImpossiblePathError(f"Can not enter cell from {entdir}.")


class SimpleTimedCrossCellElement(SimpleTimedCellElement):
    """Cell element with a paths in NS orientation, and WE orientation."""

    _view = 6

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the next cell the train will visit.

        Returns the opposite direction of the entry direction.
        """
        return -entdir


class SimpleTimedCrossBridgeCellElement(SimpleTimedCrossCellElement):
    """Overrides cross cell's view."""

    _view = 7


class SimpleTimedXJunctionCellElement(SimpleTimedCellElement):
    r"""Stateful X-Junction cell element.

    A straight path and two curved paths starting from the cell's direction exists.
    A train coming from the cell's direction is routed depending on the state of the
    junction. Trains coming from other directions are directed to the cell's direction
    regardless of the junction's state.

    You can see the ASCII illustration of the cell below.


         OPPOST
           |
       --  | -- DIVERGED
          \|/
           |
          CELL'S
          DIRECT

    """

    _view = 5

    class JunctionState(Enum):
        """Junction state enumeration."""

        # Order is important.
        STRAIGHT = 2
        CCW = 3
        CW = 1

    def __init__(self, x: int, y: int) -> None:
        """Inits the cell with position and the default state (STRAIGHT)."""
        super().__init__(x, y)
        _e = SimpleTimedXJunctionCellElement.JunctionState
        self._state_next = {_e.STRAIGHT: _e.CCW, _e.CCW: _e.CW, _e.CW: _e.STRAIGHT}
        self._state = _e.STRAIGHT

    def switch_state(self) -> None:
        """Switches the state of the X junction.

        The junction directs the train coming from the cell's direction depending on
        the state. The state follows the pattern STRAIGHT -> CCW -> CW -> STRAIGHT...
        """
        self._state = self._state_next[self._state]

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the direction the train will exit from.

        If the train came from the cell's direction, it is redirected depending on the
        junction's state. Otherwise it exits from the cell's direction regardless of the
        state.
        """
        if entdir == self.direction:
            return entdir + self._state.value
        return self.direction


class SimpleTimedYJunctionCellElement(SimpleTimedXJunctionCellElement):
    r"""Stateful Y-junction cell element. Extends X Junction.

    A straight with the same orientation as the cell and a curved path from the cell's
    direction and either to the right or to the left of the cell's direction exists.
    A train coming from the cell's direction goes straight or diverges to the curved
    path depending on the junction state. By default, the junction state directs
    trains coming from cell's direction to the straight path.

    Trains coming from the opposite of the cell's direction or the curved path's end
    go through the cell's direction regardless of the junction's state.

    You can see ASCII illustration of two possible configuration of the cell below.

          OPPOST
           |  |
       --  |  | -- DIVERGED (can be cw or ccw wrt the cell's direction.
          \|  |/
           |  |
          CELL'S
          DIRECT
    """

    def __init__(self, x: int, y: int, curve: Literal["cw", "ccw"]) -> None:
        """Inits the cell with position and default state (STRAIGHT)."""
        if curve == "cw":
            self._curve = self.JunctionState.CW
        elif curve == "ccw":
            self._curve = self.JunctionState.CCW
        else:
            raise ValueError('Argument curve must be either "cw" or "ccw"')

        super().__init__(x, y)
        self._state_next = {
            self._curve: self.JunctionState.STRAIGHT,
            self.JunctionState.STRAIGHT: self._curve,
        }

    def next_cell(self, entdir: Direction) -> Direction:
        """Returns the direction the train will exit from.

        The behavior depends on the state of the cell. If the train came from the
        cell's direction, the behavior depends on the state of the cell. If the
        train came from the other side of the straight or the curved path,
        it exists through the cell's direction regardless of the state.

        Raises ImpossiblePathError if the train came from the direction
        with no path.
        """
        # Direction implements modular addition with __add__.
        curved_end: Direction = self.direction + self._curve.value
        straight_end: Direction = self.direction + 2

        # The direction the train will leave from if coming from the cell's direction.
        stateful_end: Direction = self.direction + self._state.value

        if entdir == self.direction:
            return stateful_end
        if entdir in [curved_end, straight_end]:
            return self.direction
        # coming from the direction with no path
        raise ImpossiblePathError(f"The train could not have entered from {entdir}.")

    def get_view(self):
        """Returns view depending on the emplacement of the curved path."""
        if self._curve == self.JunctionState.CW:
            return 3, self.direction.value
        return 4, self.direction.value
