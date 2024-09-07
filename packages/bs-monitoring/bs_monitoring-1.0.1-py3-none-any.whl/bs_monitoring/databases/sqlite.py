from dataclasses import dataclass
import sqlite3

from bs_monitoring.common.utils import ConfigField
from bs_monitoring.databases.base import Database, register_database


@dataclass
class SqliteDatabaseConfig:
    """Configuration for the SQLite database.

    Args:
        path (str): The path to the SQLite database.
    """

    path: str


@register_database
class SqliteDatabase(Database):
    path = ConfigField(str)

    def __init__(self, config: SqliteDatabaseConfig) -> None:
        """SQLite database implementation.

        Args:
            config (SqliteDatabaseConfig): The configuration for the database.
        """
        super().__init__(config)
        self.conn = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.path)

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()

    def execute(self, query: str, params=None):
        cursor = self.conn.cursor()

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor

    def commit(self) -> None:
        self.conn.commit()

    @property
    def autocommit(self) -> bool:
        return self.conn.autocommit

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        self.conn.autocommit = value
