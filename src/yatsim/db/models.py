"""Model DB API for game objects."""
import pickle
import sqlite3
from copy import deepcopy
from typing import List, Optional, Tuple

from yatsim.room import Room


class ModelRoom:
    """Model API for Rooms."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Inits the model api with a connection."""
        self.conn = conn

    def create_room(self, room: Room, user_id: int) -> None:
        """Stores a new room in the DB.

        Args:
            room: New room object.
            user_id: Owner of the new room.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
        INSERT INTO room (roomName, gridData, ownerId) VALUES
        (?, ?, ?)
        """,
            (room.room_name, pickle.dumps(room.game_grid), user_id),
        ).fetchall()
        res = cur.execute(
            """
        SELECT room.id FROM room
        WHERE ownerId = (?)
        AND roomName = (?)
        """,
            (user_id, room.room_name),
        ).fetchone()
        room.room_id = res
        cur.close()

    def retrieve_room_names(self, user_id: int) -> List[Tuple[int, str]]:
        """Fetches room id - name - owner name tuples accessible by a user."""
        cur = self.conn.cursor()
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
        return res

    def retrieve_room(self, room_id: int) -> Optional[Room]:
        """Retrieves room given a room id."""
        cur = self.conn.cursor()
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
        return Room(pickle.loads(res_data[1]), res_data[0], room_id)

    def save_room(self, room: Room):
        """Updates the GameGrid data of a room."""
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE room
            SET gridData = (?)
            WHERE id = (?)
            """,
            (pickle.dumps(room.game_grid), room.room_id),
        )
        cur.close()

    def remove_room(self, room: Room):
        """Removes the room from DB."""
        cur = self.conn.cursor()
        cur.execute(
            """
            DELETE FROM room WHERE id = (?)
            """,
            (room.room_id,),
        ).fetchall()
        cur.close()

    def add_player(self, room: Room, user_id: int):
        """Allows a user to play in a room as a player."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO guest (playerId, roomId)
            VALUES (?, ?)
            """,
            (user_id, room.room_id),
        ).fetchall()
        cur.close()

    def remove_player(self, room: Room, user_id: int):
        """Disallows a user from a room."""
        cur = self.conn.cursor()
        cur.execute(
            """
            DELETE FROM guest
            WHERE playerId = (?)
            AND roomId = (?)
            """,
            (user_id, room.room_id),
        ).fetchall()
        cur.close()

    def clone_room(self, room: Room, user_id: int):
        """Clones a room owned by someone else."""
        clone_room = deepcopy(room)
        self.create_room(clone_room, user_id)
