"""The class that stores data and functions for the user."""

from typing import List, Optional, Tuple

from yatsim.db.connect import DB


class UserManager:
    """The class that stores functions related to user.

    Attributes:
        db: Needed db connection.
    """

    def __init__(self, db: DB) -> None:
        """Initializes db connection."""
        self.db = db

    def login(self, username: str, password: str) -> Optional[int]:
        """Checks database and returns user_id if the entered password is correct."""
        return self.db.user.auth_user(username, password)

    def get_game_grid_list(self, user_id: int) -> List[Tuple[int, str]]:
        """Gets all of the available room [id, name] from database and returns them."""
        return self.db.room.retrieve_room_names(user_id)

    def check_room_id(self, user_id: int, room_id: int) -> bool:
        """Checks if this user can enter a such room."""
        room_list = self.get_game_grid_list(user_id)
        return room_id in [r[0] for r in room_list]

    def add_grid(self, user_id: int, room_id: int):
        """Adds given room to a user's list."""
        self.db.room.add_player(user_id, room_id)

    def remove_grid(self, user_id: int, room_id: int):
        """Adds given room to a user's list."""
        self.db.room.remove_player(user_id, room_id)
