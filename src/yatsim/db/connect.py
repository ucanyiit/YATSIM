import os
import shutil
import sqlite3
import subprocess
from functools import cache
from sqlite3 import Connection
from typing import Optional, Union, cast

if shutil.which("sqlite3") is None:
    raise ImportError(
        "sqlite3 could not be found. Make sure sqlite3 is installed and is in your "
        "PATH variable."
    )

SQL_EXECUTABLE = cast(str, shutil.which("sqlite3"))


class DB:
    configured: bool = False
    db_path: str = ""

    @classmethod
    def connect(cls):
        if cls.configured:
            return sqlite3.connect(cls.db_path)
        raise sqlite3.DatabaseError(
            "DB class should be configured with DB.initial_connect() first."
        )

    @classmethod
    def initial_connect(
        cls, db_path: Optional[str] = None, create_new: bool = True
    ) -> Connection:
        if DB._determine_path(db_path) is None:
            raise ValueError(
                "Neither arg 'db_path' nor env 'DB_PATH' was given in strict mode."
            )
        if not (os.path.exists(str(db_path)) or create_new):
            raise OSError(f"Given path {db_path} does not exist.")
        db_path_str = cast(str, db_path)
        db_chk = subprocess.run(
            [SQL_EXECUTABLE, db_path_str, ".databases"],
            text=True,
            check=True,
            capture_output=True,
        )
        if db_chk.stdout == "":
            raise sqlite3.DatabaseError(
                f"Error executing '.databases' on {db_path} "
                f"with executable {SQL_EXECUTABLE}: db_chk."
            )
        conn = sqlite3.connect(db_path_str)
        cls._check_tables(conn)
        conn.commit()
        cls.db_path = db_path_str
        cls.configured = True
        return conn

    @staticmethod
    @cache
    def _determine_path(db_path: Union[str, bytes, None]) -> Union[str, bytes, None]:
        env_db_path = os.getenv("DB_PATH")
        return db_path if db_path is not None else env_db_path

    @classmethod
    def _check_tables(cls, conn: Connection):
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
