"""The class that manages connections/requests for GameGrid."""

from threading import Lock
from typing import Dict

from server import Connection
from yatsim.cell.cell_element import Direction
from yatsim.cell.cell_factory import SimpleTimedCellFactory
from yatsim.game_grid import GameGrid


class Room:
    """The class that manages connections/requests for GameGrid.

    Attributes:
        connections: A list that stores connection information. (Includes
        user and socket info)
        game_grid: The game grid object that is shared between players.
        lock: A simple lock for each room that ensures that requests are
        handled in order.
    """

    # Creates a train at given cell with given number of cars behind. The total size of
    # train is ncars+1 including the engine.
    def __init__(self, game_grid: GameGrid) -> None:
        """Inits train with type, number of cars and the initial cell."""
        self.connections: Dict[str, Connection] = {}
        self.game_grid: GameGrid = game_grid
        self.lock: Lock = Lock()

    def connect(self, username: str, s: Connection):
        """Connect a new user to the room."""
        with self.lock:
            self.connections[username] = s
            return self.game_grid.view

    def disconnect(self, username: str) -> int:
        """Disconnect a user from the room."""
        with self.lock:
            del self.connections[username]
            return len(self.connections)

    def send_update(self, update: Dict) -> None:
        """Send an update to all users in the room."""
        for connection in self.connections.values():
            connection.send_update(update)

    def send_updated_cell(self, x: int, y: int) -> None:
        """Send the information related to a cell which is recently updated."""
        view = self.game_grid.elements[y][x].get_view()
        self.send_update(
            {
                "type": "UPDATE",
                "x": x,
                "y": y,
                "view": view,
            }
        )

    def handle_switch(self, x: int, y: int) -> None:
        """Handles switch operation on a cell."""
        with self.lock:
            self.game_grid.elements[y][x].switch_state()
            self.send_updated_cell(x, y)

    def handle_rotate(self, x: int, y: int, direction: Direction) -> None:
        """Handles rotate operation on a cell."""
        with self.lock:
            self.game_grid.elements[y][x].set_direction(direction)
            self.send_updated_cell(x, y)

    def handle_place(self, x: int, y: int, cell_type: int) -> None:
        """Handles a place operation."""
        with self.lock:
            self.game_grid.elements[y][x] = SimpleTimedCellFactory().new(
                x, y, cell_type
            )
            self.send_updated_cell(x, y)

    def handle_place_rotated(
        self, x: int, y: int, cell_type: int, direction: int
    ) -> None:
        """Handles a place operation operation with direction."""
        with self.lock:
            self.game_grid.elements[y][x] = SimpleTimedCellFactory().rotated_new(
                x, y, cell_type, direction
            )
            self.send_updated_cell(x, y)
