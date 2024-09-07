from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from bs_monitoring.alert_services import AlertService
from bs_monitoring.common.utils import register_config


@dataclass
class DataSourceConfig:
    """Configuration for the data source component

    Args:
        type (str): The type of the data source.
        config (Union[ElasticDataSourceConfig, None], optional): The configuration for the data source. Defaults to None.
    """

    type: str
    config: None = None


class DataSource(ABC):
    def __init__(self, config: Any) -> None:
        for k, v in asdict(config).items():
            setattr(self, k, v)

    @abstractmethod
    def produce(
        self,
    ) -> dict[str, list[dict[str, Any]]]:
        """Method to produce data from the data source.

        Returns:
            Dict[str, List[Dict[str, Any]]]: The data produced. The keys are the indices and the values are the messages.
        """
        pass


def register_data_source(cls):
    assert issubclass(
        cls, DataSource
    ), f"Class {cls.__name__} must be a subclass of DataSource to be registered as one."

    name = (
        cls.__name__
        if not cls.__name__.endswith("DataSource")
        else cls.__name__.removesuffix("DataSource")
    )
    __DATA_SOURCES[name] = cls
    register_config(cls, DataSourceConfig)
    return cls


__DATA_SOURCES = {}


def create_data_source(
    config: DataSourceConfig, alert_service: AlertService
) -> DataSource:
    """Create a data source based on the configuration.

    Args:
        config (DataSourceConfig): The configuration for the data source.
        alert_service (AlertService): The alert service to use.

    Raises:
        Exception: If the data source type is unknown.

    Returns:
        DataSource: The data source subclass instance.
    """
    c = config.config if hasattr(config, "config") else None

    src = __DATA_SOURCES.get(config.type)
    if src is not None:
        return src(alert_service, c)
    else:
        raise Exception(f"Unknown data source type: {config.type}")
