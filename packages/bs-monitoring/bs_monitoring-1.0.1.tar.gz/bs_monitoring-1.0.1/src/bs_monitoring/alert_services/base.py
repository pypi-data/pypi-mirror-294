from abc import ABC, abstractmethod
import functools
import json
from typing import Any, Callable
from bs_monitoring.common.utils import MonitoringServiceError, register_config
from dataclasses import dataclass, asdict


@dataclass
class AlertServiceConfig:
    """Configuration for the alert service component

    Args:
        type (str): The type of the alert service.
        config (Union[OpsgenieAlertServiceConfig, None], optional): The configuration for the alert service. Defaults to None.
    """

    type: str
    config: None = None


class AlertService(ABC):
    """Abstract class for alert services."""

    def __init__(self, config: Any) -> None:
        for k, v in asdict(config).items():
            setattr(self, k, v)

    @abstractmethod
    def send_alert(
        self,
        message: str,
        description: str | None = None,
    ):
        """Method to send an alert.

        Args:
            message (str): The message for the alert.
            description (Optional[str], optional): Extra description for the alert. Defaults to None.
        """
        pass


def alert(
    message: str,
) -> Callable:
    """Decorator to send an alert if an exception is raised.

    Args:
        message (str): The message to send in the alert.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except MonitoringServiceError as e:
                alert_service: AlertService = self.alert_service
                context = {
                    "class": self.__class__.__name__,
                    "method": func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                    "error": str(e),
                }
                context = json.dumps(context)
                alert_service.send_alert(
                    message=message,
                    description=context,
                )
            except Exception as e:
                raise e

        return inner

    return decorator


def register_alert_service(cls):
    assert issubclass(
        cls, AlertService
    ), "AlertService must be a subclass of AlertService"

    name = (
        cls.__name__
        if not cls.__name__.endswith("AlertService")
        else cls.__name__.removesuffix("AlertService")
    )
    __ALERT_SERVICES[name] = cls
    register_config(cls, AlertServiceConfig)
    return cls


__ALERT_SERVICES = {}


def create_alert_service(config: AlertServiceConfig) -> AlertService:
    """Create an alert service based on the configuration.

    Args:
        config (AlertServiceConfig): The configuration for the alert service.

    Raises:
        Exception: If the alert service type is unknown.

    Returns:
        AlertService: The alert service subclass instance.
    """
    c = config.config if hasattr(config, "config") else None

    svc = __ALERT_SERVICES.get(config.type)
    if svc is not None:
        return svc(c)
    else:
        raise Exception(f"Unknown alert service type: {config.type}")
