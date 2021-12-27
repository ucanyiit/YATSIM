"""The class that stores data and functions for the user."""

from typing import List


class UserManager:
    """The class that stores functions related to user.

    Attributes:
        none
    """

    def __init__(self) -> None:
        """Nothing rn."""
        pass

    def login(self, username: str, password: str) -> bool:
        """Checks database and return True if the entered password is correct."""
        # actual_password = getPasswordFromDB(username)
        username += "asd"  # remove this
        return "passwordFromDB" == password

    def get_game_grid_list(self, username: str) -> List[str]:
        """Gets all of the available grid names from database and returns them."""
        # result = getPasswordFromDB(username)
        username += "asd"  # remove this
        return []

    def check_room_id(self, username: str, room_id: str) -> bool:
        """Checks if this user in a such room."""
        # result = checkUserRoomList(username, room_id)
        username += "asd"  # remove this
        room_id += "asd"  # remove this
        return True

    def add_grid(self, username: str, room_id: str):
        """Adds given room to a user's list."""
        # insertRoomIdToUserList(username, room_id)
        username += "asd"  # remove this
        room_id += "asd"  # remove this

    def remove_grid(self, username: str, room_id: str):
        """Adds given room to a user's list."""
        # removeRoomIdToUserList(username, room_id)
        username += "asd"  # remove this
        room_id += "asd"  # remove this
