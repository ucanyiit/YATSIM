"""Database schema utility class module."""

from sqlite3 import Connection


class DBSchema:
    """Utility class for checking and creating tables."""

    @classmethod
    def check_tables(cls, conn: Connection):
        """Check and create tables, given a Connection object.

        Columns of the tables are not checked. Either drop and recreate the table or
        manually modify the table if this is the case.
        """
        cur = conn.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_schema")]
        if "user" not in tables:
            cls._create_user(conn)
        if "room" not in tables:
            cls._create_room(conn)
        if "guest" not in tables:
            cls._create_guest(conn)
        if "player" not in tables:
            cls._create_player(conn)
        if "index_username" not in tables:
            cls._create_username_index(conn)
        conn.commit()
        cur.close()

    @staticmethod
    def _create_user(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            """
        )
        cur.close()

    @staticmethod
    def _create_room(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE room (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roomName TEXT NOT NULL,
                ownerId INTEGER NOT NULL,
                gridData BLOB NOT NULL,
                UNIQUE (roomName, ownerId),
                FOREIGN KEY(ownerid) REFERENCES user(id)
            );
            """
        )
        cur.close()

    @staticmethod
    def _create_guest(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE guest (
                playerId INTEGER NOT NULL,
                roomId INTEGER NOT NULL,
                FOREIGN KEY (playerId) references user(id),
                FOREIGN KEY (roomId) references room(id),
                PRIMARY KEY (playerId, roomId)
            );
            """
        )
        cur.close()

    @staticmethod
    def _create_player(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE VIEW players AS
                SELECT roomId, playerId FROM guest
                UNION
                SELECT id, ownerId FROM room;
            """
        )
        cur.close()

    @staticmethod
    def _create_username_index(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE UNIQUE INDEX index_username on user (username);
            """
        )
        cur.close()
