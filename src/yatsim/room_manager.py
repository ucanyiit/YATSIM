"""The class that manages connections/requests for GameGrid."""

from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict

from yatsim.db.connect import DB
from yatsim.game_grid import GameGrid
from yatsim.room import Room

if TYPE_CHECKING:
    from yatsim.connection import Connection


class RoomManager:
    """The class that manages connections/requests for GameGrid.

    Attributes:
        rooms: The dictionary in which all active rooms are stored.
        lock: A simple lock for each room that ensures that requests are
        handled in order.
        db: Needed db connection.
    """

    def __init__(self, db: DB) -> None:
        """Inits RoomManager with the empty dictionary."""
        self.rooms: Dict[int, Room] = {}
        self.lock: Lock = Lock()
        self.db = db

    def connect(self, username: str, connection: Connection, room_id: int):
        """Connect a new user to a room."""
        with self.lock:
            if room_id not in self.rooms:
                room = self.db.room.retrieve_room(room_id, self.db)
                if not room:
                    raise Exception("No such room in database.")
                self.rooms[room.room_id] = room

        self.rooms[room_id].connect(username, connection)
        return self.rooms[room_id]

    def disconnect(self, username: str, room_id: int) -> None:
        """Disconnect a user from a room."""
        with self.lock:
            if room_id not in self.rooms:
                raise Exception("Room is not available")

        remaining_user_count = self.rooms[room_id].disconnect(username)

        with self.lock:
            if remaining_user_count == 0:
                del self.rooms[room_id]

    def create_game_grid(self, height: int, width: int, name: str, user_id: int):
        """Initializes a room by saving it into the DB."""
        with self.lock:
            game_grid = GameGrid(height, width)
            room = Room(game_grid, name, self.db)

            self.db.room.create_room(room, user_id)
            return room.room_id
