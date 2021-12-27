"""The class that manages connections/requests for GameGrid."""

from threading import Lock
from typing import Dict

from server import Connection
from yatsim.game_grid import GameGrid

# from yatsim.game_grid import GameGrid
from yatsim.roomm import Room


class RoomManager:
    """The class that manages connections/requests for GameGrid.

    Attributes:
        rooms: The dictionary in which all active rooms are stored.
        lock: A simple lock for each room that ensures that requests are
        handled in order.
    """

    def __init__(self) -> None:
        """Inits RoomManager with the empty dictionary."""
        self.rooms: Dict[str, Room] = {}
        self.lock: Lock = Lock()

    def connect(self, username: str, connection: Connection, room_id: str):
        """Connect a new user to a room."""
        with self.lock:
            if room_id not in self.rooms:
                # game_grid = getGameGridFromDB
                # self.rooms[room_id] = Room(game_grid)
                pass

        self.rooms[room_id].connect(username, connection)
        return self.rooms[room_id]

    def disconnect(self, username: str, room_id: str) -> None:
        """Disconnect a user from a room."""
        with self.lock:
            if room_id not in self.rooms:
                raise Exception("Room is not available")

            remaining_user_count = self.rooms[room_id].disconnect(username)

            if remaining_user_count == 0:
                del self.rooms[room_id]

    def create_game_grid(self, height: int, width: int):
        """Initializes a room by saving it into the DB."""
        with self.lock:
            # game_grid =
            GameGrid(height, width)
            room_id = "asd"
            # saveGameGridToDB(room_id, game_grid)
            return room_id
