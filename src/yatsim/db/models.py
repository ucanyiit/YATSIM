"""Model DB API for game objects."""
import pickle
import sqlite3
from typing import List, Optional, Tuple

from yatsim.room import Room


class ModelRoom:
    """Model API for Rooms."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Inits the model api with a connection."""
        self.conn = conn

    def create_room(self, room: Room, username: str) -> None:
        """Stores a new room in the DB.

        Args:
            room: New room object.
            username: Owner of the new room.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
        INSERT INTO room (roomName, gridData, ownerId) VALUES
        (?, ?, (SELECT username FROM user where username = ?))
        """,
            (room.room_name, pickle.dumps(room.game_grid), username),
        ).fetchall()
        res = cur.execute(
            """
        SELECT room.id FROM room
        JOIN user on room.ownerId = user.id
        WHERE user.username = (?)
        AND room.roomName = (?)
        """,
            (username, room.room_name),
        ).fetchone()
        room.room_id = res
        cur.close()

    def retrieve_room_names(self, username: str) -> List[Tuple[int, str]]:
        """Fetches room id-roomName-ownerName tuples accessible by a user."""
        cur = self.conn.cursor()
        res = cur.execute(
            """
            SELECT r.id, r.roomName, o.username FROM player p
            JOIN user u ON u.id = p.playerId
            JOIN room r ON p.roomId = r.id
            JOIN user o ON r.ownerId = o.id
            WHERE u.username = (?)
            """,
            (username,),
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
