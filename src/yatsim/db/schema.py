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
        if "grid" not in tables:
            cls._create_grid(conn)
        if "game" not in tables:
            cls._create_game(conn)
        if "guest" not in tables:
            cls._create_guest(conn)
        if "player" not in tables:
            cls._create_player(conn)
        if "index_username" not in tables:
            cls._create_username_index(conn)

    @staticmethod
    def _create_user(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            );
            """
        )

    @staticmethod
    def _create_grid(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE grid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gridData BLOB
            );
            """
        )

    @staticmethod
    def _create_game(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE game (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gameName TEXT,
                ownerId INTEGER,
                private INTEGER,
                FOREIGN KEY(ownerid) REFERENCES user(id)
            );
            """
        )

    @staticmethod
    def _create_guest(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE guest (
                playerId INTEGER,
                gameId INTEGER,
                FOREIGN KEY (playerId) references user(id),
                FOREIGN KEY (gameId) references game(id),
                PRIMARY KEY (playerId, gameId)
            );
            """
        )

    @staticmethod
    def _create_player(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE VIEW players AS
                SELECT * FROM guests
                UNION
                SELECT id, ownerId FROM game;
            """
        )

    @staticmethod
    def _create_username_index(conn: Connection):
        cur = conn.cursor()
        cur.execute(
            """
            CREATE UNIQUE INDEX index_username on user (username);
            """
        )
