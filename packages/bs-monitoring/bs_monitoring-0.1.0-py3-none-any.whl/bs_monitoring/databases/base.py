from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from bs_monitoring.common.utils import register_config


@dataclass
class DatabaseConfig:
    type: str
    name: str
    config: None = None


class Database(ABC):
    def __init__(self, config: Any):
        for k, v in asdict(config).items():
            setattr(self, k, v)

    @abstractmethod
    def connect(self) -> None:
        """Method to connect to the database."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Method to close the connection to the database."""
        pass

    @abstractmethod
    def execute(self, query: str) -> None:
        """Method to execute a query on the database.

        Args:
            query (str): The query to execute.
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """Method to commit the transaction."""
        pass

    @property
    def autocommit(self) -> bool:
        """Property to get the autocommit status of the connection."""
        pass

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        """Property to set the autocommit status of the connection.

        Args:
            value (bool): The value to set.
        """
        pass


def register_database(cls):
    assert issubclass(
        cls, Database
    ), f"Class {cls.__name__} must be a subclass of Database"

    name = (
        cls.__name__
        if not cls.__name__.endswith("Database")
        else cls.__name__.removesuffix("Database")
    )
    DATABASES[name] = cls
    register_config(cls, DatabaseConfig)
    return cls


DATABASES: dict[str, Database] = {}


class DatabaseContext:
    _instance = None
    _db_connections: dict[str, Database] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseContext, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, name, db_type, config):
        conn: Database = DATABASES[db_type](config)
        conn.connect()
        cls._db_connections[name] = conn

    @classmethod
    def get_connection(cls, name):
        if name not in cls._db_connections:
            raise RuntimeError(f"Database connection {name} not initialized")
        return cls._db_connections[name]

    @classmethod
    def close_all(cls):
        for c in cls._db_connections.values():
            c.close()
        cls._db_connections.clear()


def initialize_databases(configs: list[DatabaseConfig]) -> None:
    for config in configs:
        DatabaseContext.initialize(config.name, config.type, config.config)
