from typing import Any
from bs_monitoring.common.utils import MonitoringServiceError, ConfigField
from bs_monitoring.alert_services import alert, AlertService
from cerberus import Validator
import yaml

from bs_monitoring.monitors.base import Monitor, register_monitor


class DataSchemeError(MonitoringServiceError):
    def __init__(self, message: str) -> None:
        """Exception raised when there is an error in the data scheme.

        Args:
            message (str): The error message.
        """
        super().__init__(message)


@register_monitor
class DataSchemeMonitor(Monitor):
    file = ConfigField(str)

    def __init__(
        self,
        alert_service: AlertService,
        db_name: str | None = None,
        config: Any = None,
    ) -> None:
        """Monitor to check the data scheme of the data.

        Args:
            alert_service (AlertService): The alert service to use.
            config (DataSchemeMonitorConfig): The configuration for the monitor.
        """
        super().__init__(alert_service, db_name, config)

        with open(self.file, "r") as f:
            self.validator_ = Validator(yaml.safe_load(f), allow_unknown=True)

    @alert(message="Data scheme error")
    def process(self, data: dict[str, Any]) -> None:
        """Method to process the data, sends an alert if the data does not match the data scheme.

        Args:
            data (Dict[str, Any]): The data to process.

        Raises:
            DataSchemeError: Raised if the data does not match the data scheme.
        """
        for k, v in data.items():
            invalid_items = list(filter(lambda x: not self.validator_.validate(x), v))
            if len(invalid_items) > 0:
                raise DataSchemeError(
                    f"Data scheme error {self.validator_.errors} for {k}: {invalid_items}"
                )
