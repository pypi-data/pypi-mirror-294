from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any

from bs_monitoring.alert_services.base import AlertService
from bs_monitoring.databases.base import DatabaseContext
from bs_monitoring.common.utils import register_config


@dataclass
class MonitorConfig:
    """Configuration for the monitor component

    Args:
        type (str): The type of the monitor.
        config (Union[DataSchemeMonitorConfig, None], optional): The configuration for the monitor. Defaults to None.
    """

    type: str
    db_name: str | None = None
    config: None = None


class Monitor(ABC):
    def __init__(
        self,
        alert_service: AlertService,
        db_name: str | None = None,
        config: Any = None,
    ) -> None:
        """Abstract class for monitors.

        Args:
            alert_service (AlertService): The alert service to use.
        """
        self.alert_service = alert_service
        self.connection = DatabaseContext.get_connection(db_name) if db_name else None

        for k, v in asdict(config).items():
            setattr(self, k, v)

    @abstractmethod
    def process(self, data: dict[str, Any]) -> None:
        """Method to process the data and send alerts if necessary.

        Args:
            data (Dict[str, Any]): The data to process.
        """
        pass


def register_monitor(cls: type[Monitor]) -> type[Monitor]:
    """Decorator to register a monitor.

    Args:
        cls (Monitor): Subclass of Monitor to register.

    Returns:
        Monitor: The registered Monitor subclass.
    """
    assert issubclass(
        cls, Monitor
    ), f"Class {cls.__name__} must be a subclass of Monitor to be registered as one."
    name = (
        cls.__name__
        if not cls.__name__.endswith("Monitor")
        else cls.__name__.removesuffix("Monitor")
    )

    __MONITORS[name] = cls
    register_config(cls, MonitorConfig)
    return cls


__MONITORS = {}


def create_monitors(
    configs: list[MonitorConfig], alert_service: AlertService
) -> list[Monitor]:
    """Method to create a monitor instances based on the configuration.

    Args:
        configs (List[MonitorConfig]): The configuration for the different monitors.
        alert_service (AlertService): The alert service to use.

    Returns: List[Monitor]: The list of monitor instances.
    """
    monitors = []
    for config in configs:
        c = getattr(config, "config", None)
        m = __MONITORS[config.type](alert_service, config.db_name, c)
        monitors.append(m)

    return monitors
