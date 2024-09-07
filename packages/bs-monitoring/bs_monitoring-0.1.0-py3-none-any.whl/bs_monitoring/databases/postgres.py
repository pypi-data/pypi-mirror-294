from typing import Any
import psycopg2

from bs_monitoring.common.utils import ConfigField
from bs_monitoring.databases.base import Database, register_database


@register_database
class PostgresDatabase(Database):
    host = ConfigField(str)
    port = ConfigField(int)
    user = ConfigField(str)
    password = ConfigField(str)
    database = ConfigField(str)

    def __init__(self, config: Any) -> None:
        self.config = config
        self.conn = None

    def connect(self) -> None:
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()

    def execute(self, query: str, params=None) -> None:
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
