"""Default Cell factories are defined here."""

from typing import Any, overload

from .cell_element import (
    CellElement,
    SimpleTimedBackgroundCellElement,
    SimpleTimedCellElement,
    SimpleTimedCrossBridgeCellElement,
    SimpleTimedCrossCellElement,
    SimpleTimedCurvedCellElement,
    SimpleTimedStation,
    SimpleTimedStraightCellElement,
    SimpleTimedXJunctionCellElement,
    SimpleTimedYJunctionCellElement,
)


class CellFactory:
    """Abstract factory for creating cell objects."""

    def new(self, x: int, y: int, cell_type: Any, *args, **kwargs) -> CellElement:
        """Creates a new cell.

        Subclasses are required to implement this method.
        """
        raise NotImplementedError()


class SimpleTimedCellFactory(CellFactory):
    """A basic factory for demonstration purposes."""

    @overload
    def new(
        self, x: int, y: int, cell_type: str, *args, **kwargs
    ) -> SimpleTimedCellElement:
        pass

    @overload
    def new(
        self, x: int, y: int, cell_type: int, *args, **kwargs
    ) -> SimpleTimedCellElement:
        pass

    def new(self, x, y, cell_type, *args, **kwargs) -> SimpleTimedCellElement:
        """Returns a SimpleTimedCell."""
        if isinstance(cell_type, str):
            if cell_type == "bg":
                return SimpleTimedBackgroundCellElement(x, y)
            if cell_type == "strt":
                return SimpleTimedStraightCellElement(x, y)
            if cell_type == "curv":
                return SimpleTimedCurvedCellElement(x, y)
            if cell_type == "cross":
                return SimpleTimedCrossCellElement(x, y)
            if cell_type == "x":
                return SimpleTimedXJunctionCellElement(x, y)
            if cell_type == "y":
                return SimpleTimedYJunctionCellElement(x, y, kwargs["curve_dir"])
            raise ValueError('cell_type must be one of "bg", "strt", "curv", "x", "y"')
        if isinstance(cell_type, int):
            if cell_type == 1:
                return SimpleTimedStraightCellElement(x, y)

            if cell_type == 2:
                return SimpleTimedCurvedCellElement(x, y)

            if cell_type == 3:
                return SimpleTimedYJunctionCellElement(x, y, "cw")

            if cell_type == 4:
                return SimpleTimedYJunctionCellElement(x, y, "ccw")

            if cell_type == 5:
                return SimpleTimedXJunctionCellElement(x, y)

            if cell_type == 6:
                return SimpleTimedCrossCellElement(x, y)

            if cell_type == 7:
                return SimpleTimedCrossBridgeCellElement(x, y)

            if cell_type == 8:
                return SimpleTimedStation(x, y)
            raise ValueError("cell_type must be a int from 1 to 8.")
        raise TypeError("cell_type must be an int or str.")
