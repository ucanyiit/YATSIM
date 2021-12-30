"""The class that manages connections/requests for GameGrid."""

from threading import Lock
from typing import Dict, List, Tuple

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

    def __init__(self, room_id: str) -> None:
        """Inits Room with the given game grid object."""
        self.connections: Dict[str, Connection] = {}
        room_id += "1"  # remove
        # game_grid = getGameGridFromDB(room_id)
        # self.game_grid: GameGrid = game_grid
        self.game_grid: GameGrid = GameGrid(2, 2, self)
        self.lock: Lock = Lock()

    def _send_update(self, update: Dict) -> None:
        """Send an update to all users in the room."""
        for connection in self.connections.values():
            connection.send_update(update)

    def _send_updated_cell(self, x: int, y: int) -> None:
        """Send the information related to a cell which is recently updated."""
        view = self.game_grid.elements[y][x].get_view()
        self._send_update(
            {
                "type": "UPDATE",
                "x": x,
                "y": y,
                "view": view,
            }
        )

    def _send_updated_trains(self) -> None:
        """Send the information related to a cell which is recently updated."""
        geometries: List[Tuple[int, int, int, int]] = self.game_grid.get_trains()
        self._send_update(
            {
                "type": "TRAINS",
                "trains": geometries,
            }
        )

    def connect(self, username: str, connection: Connection):
        """Connect a new user to the room."""
        with self.lock:
            self.connections[username] = connection
            self.connections[username].send_message(
                {
                    "type": "VIEW",
                    "view": self.game_grid.display(),
                    "height": self.game_grid.height,
                    "width": self.game_grid.width,
                }
            )

    def disconnect(self, username: str) -> int:
        """Disconnect a user from the room."""
        with self.lock:
            del self.connections[username]
            return len(self.connections)

    def handle_start_simulation(self) -> None:
        """Handles start operation on a simulation."""
        with self.lock:
            self.game_grid.start_simulation()

    def handle_stop_simulation(self) -> None:
        """Handles stop operation on a simulation."""
        with self.lock:
            self.game_grid.stop_simulation()

    def handle_toggle_simulation(self) -> None:
        """Handles toggle operation on a simulation."""
        with self.lock:
            self.game_grid.set_pause_resume()

    def handle_switch(self, x: int, y: int) -> None:
        """Handles switch operation on a cell."""
        with self.lock:
            self.game_grid.elements[y][x].switch_state()
            self._send_updated_cell(x, y)

    def handle_rotate(self, x: int, y: int, direction: Direction) -> None:
        """Handles rotate operation on a cell."""
        with self.lock:
            self.game_grid.elements[y][x].set_direction(direction)
            self._send_updated_cell(x, y)

    def handle_place(self, x: int, y: int, cell_type: int) -> None:
        """Handles a place operation."""
        with self.lock:
            self.game_grid.elements[y][x] = SimpleTimedCellFactory().new(
                x, y, cell_type
            )
            self._send_updated_cell(x, y)

    def handle_place_rotated(
        self, x: int, y: int, cell_type: int, direction: int
    ) -> None:
        """Handles a place operation operation with direction."""
        with self.lock:
            self.game_grid.elements[y][x] = SimpleTimedCellFactory().rotated_new(
                x, y, cell_type, direction
            )
            self._send_updated_cell(x, y)

    def step(self):
        """Steps the simulation once and notifies everyone."""
        with self.lock:
            self.game_grid.move_trains()
            self._send_updated_trains()
