"""Database utility class for connections and model API."""

import os
import shutil
import sqlite3
import subprocess
from sqlite3 import Connection
from typing import Optional, Union, cast

from .models import ModelRoom, ModelUser
from .schema import DBSchema

if shutil.which("sqlite3") is None:
    raise ImportError(
        "sqlite3 could not be found. Make sure sqlite3 is installed and is in your "
        "PATH variable."
    )

SQL_EXECUTABLE = cast(str, shutil.which("sqlite3"))


class DB:
    """Database utility class.

    Use this class for interfacing with the database.
    """

    def connect(self) -> Connection:
        """Creates a new Connection object."""
        return self._connect()

    def __init__(self, db_path: Optional[str] = None, create_new: bool = True) -> None:
        """Makes necessary checks and initializes a DB util object.

        This method should be used for connecting to the database for the first time.
        - Checks whether `sqlite3` is in PATH
        - Determines the path of the db by checking DB_PATH environment variable and
        db_path argument (db_path takes precedence)
        - Checks the existence of the db file
        - Creates a new db if create_new is true and the db file does not exist.
        - Creates a subprocess to check whether it is a database file.
        - Checks the table names (not columns!) of the db and creates missing tables,
        views, and indexes, and
        - Returns a new connection.

        Arguments:
            db_path: path of the db
            create_new: whether to create a new db if path does not exist

        Raises:
            ValueError: if both db_path arg is None and DB_PATH environment variable
                is not set.
            OSError: if create_new is false and db_path path does not exist.
            DatabaseError: if db given by db_path is not a db file.
        """
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
        conn = self._connect()
        DBSchema.check_tables(conn)
        conn.commit()
        self.room = ModelRoom(conn)
        self.user = ModelUser(conn)
        self._db_path = db_path_str

    @staticmethod
    def _determine_path(db_path: Union[str, bytes, None]) -> Union[str, bytes, None]:
        env_db_path = os.getenv("DB_PATH")
        return db_path if db_path is not None else env_db_path

    def _connect(self):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys=ON;")
        with cur:
            print("hi")
        cur.close()
        return sqlite3.connect(self._db_path)
