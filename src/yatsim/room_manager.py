"""The class that manages connections/requests for GameGrid."""

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from yatsim.connection import Connection
    from yatsim.room import Room

# from yatsim.game_grid import GameGrid


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
                # self.rooms[room_id] = Room(room_id)
                pass

        self.rooms[room_id].connect(username, connection)
        return self.rooms[room_id]

    def disconnect(self, username: str, room_id: str) -> None:
        """Disconnect a user from a room."""
        with self.lock:
            if room_id not in self.rooms:
                raise Exception("Room is not available")

        remaining_user_count = self.rooms[room_id].disconnect(username)

        with self.lock:
            if remaining_user_count == 0:
                del self.rooms[room_id]

    def create_game_grid(self, height: int, width: int):
        """Initializes a room by saving it into the DB."""
        with self.lock:
            height += 1
            width += 1
            room_id = "asd"
            # createGameGridOnDB(room_id, game_grid)
            return room_id
