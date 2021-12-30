"""Model DB API for game objects."""
from __future__ import annotations

import pickle
from copy import deepcopy
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from yatsim.db.connect import DB
    from yatsim.room import Room


class Model:
    """Model base class."""

    def __init__(self, db: DB) -> None:
        """Inits the model api with a connection."""
        self.db = db


class ModelRoom(Model):
    """Model API for Rooms."""

    def create_room(self, room: Room, user_id: int) -> None:
        """Stores a new room in the DB.

        Args:
            room: New room object.
            user_id: Owner of the new room.
        """
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
        INSERT INTO room (roomName, gridData, ownerId) VALUES
        (?, ?, ?)
        """,
            (room.room_name, pickle.dumps(room.game_grid), user_id),
        )
        res = cur.execute(
            """
        SELECT room.id FROM room
        WHERE ownerId = (?)
        AND roomName = (?)
        """,
            (user_id, room.room_name),
        ).fetchone()
        room.room_id = res[0] if res else None
        cur.close()
        conn.commit()
        conn.close()

    def retrieve_room_names(self, user_id: int) -> List[Tuple[int, str]]:
        """Fetches room id - name - owner name tuples accessible by a user."""
        conn = self.db.connect()
        cur = conn.cursor()
        res = cur.execute(
            """
            SELECT r.id, r.roomName, o.username FROM player p
            JOIN room r ON p.roomId = r.id
            JOIN user o ON r.ownerId = o.id
            WHERE p.playerId = (?)
            """,
            (user_id,),
        ).fetchall()
        cur.close()
        conn.close()
        return res

    def retrieve_room(self, room_id: int, db: DB) -> Optional[Room]:
        """Retrieves room given a room id."""
        conn = self.db.connect()
        cur = conn.cursor()
        res: List[Tuple[str, bytes]] = cur.execute(
            """
            SELECT roomName, gridData FROM room
            WHERE id = (?)
            """,
            (room_id,),
        ).fetchall()
        if not res:
            return None
        res_data = res[0]
        cur.close()
        conn.close()
        return Room(pickle.loads(res_data[1]), res_data[0], db, room_id)

    def save_room(self, room: Room):
        """Updates the GameGrid data of a room."""
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE room
            SET gridData = (?)
            WHERE id = (?)
            """,
            (pickle.dumps(room.game_grid), room.room_id),
        )
        cur.close()
        conn.commit()
        conn.close()

    def remove_room(self, room: Room):
        """Removes the room from DB."""
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM room WHERE id = (?)
            """,
            (room.room_id,),
        )
        cur.close()
        conn.commit()
        conn.close()

    def add_player(self, room_id: int, user_id: int):
        """Allows a user to play in a room as a player."""
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO guest (playerId, roomId)
            VALUES (?, ?)
            """,
            (user_id, room_id),
        )
        cur.close()
        conn.commit()
        conn.close()

    def remove_player(self, room_id: int, user_id: int):
        """Disallows a user from a room."""
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM guest
            WHERE playerId = (?)
            AND roomId = (?)
            """,
            (user_id, room_id),
        )
        cur.close()
        conn.commit()
        conn.close()

    def clone_room(self, room: Room, user_id: int):
        """Clones a room owned by someone else."""
        clone_room = deepcopy(room)
        self.create_room(clone_room, user_id)


class ModelUser(Model):
    """Model for user registry and authentication operations."""

    def create_user(self, username: str, password: str) -> int:
        """Creates a new user and returns its id."""
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO user (username, password)
            VALUES (?, ?)
            """,
            (username, password),
        )
        res = cur.execute(
            """
            SELECT id FROM user
            WHERE username = (?)
            """,
            (username,),
        ).fetchone()
        cur.close()
        conn.commit()
        conn.close()
        return res[0] if res else None

    def auth_user(self, username: str, password: str) -> Optional[int]:
        """Authenticates the user and returns the user id."""
        conn = self.db.connect()
        cur = conn.cursor()
        res: Optional[Tuple[int]] = cur.execute(
            """
            SELECT id FROM user
            WHERE username = (?)
            AND password = (?)
            """,
            (username, password),
        ).fetchone()
        cur.close()
        conn.close()
        return res[0] if res else None
