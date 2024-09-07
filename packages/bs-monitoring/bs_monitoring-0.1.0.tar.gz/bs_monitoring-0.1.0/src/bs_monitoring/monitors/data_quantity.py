from typing import Any
from bs_monitoring.alert_services import alert, AlertService
from bs_monitoring.common.utils import MonitoringServiceError
import pytz
from datetime import datetime, timedelta

from bs_monitoring.monitors import Monitor, register_monitor


class DataQuantityError(MonitoringServiceError):
    def __init__(self, message: str) -> None:
        """Exception raised when data quantity is 0.

        Args:
            message (str): The error message.
        """
        super().__init__(message)


@register_monitor
class DataQuantityMonitor(Monitor):
    def __init__(
        self,
        alert_service: AlertService,
        config: None = None,
        db_name: str | None = None,
    ) -> None:
        """Monitor to check the quantity of data.

        Args:
            alert_service (AlertService): The alert service to use.
            config (None, optional): No purpose, required because of the factory method. Defaults to None.
        """
        super().__init__(alert_service, db_name)

    @alert(message="Data quantity error")
    def process(self, data: dict[str, Any]) -> None:
        """Method to process the data, sends an alert if the data date is a weekday and the data quantity is 0.

        Args:
            data (Dict[str, Any]): The data to process.

        Raises:
            DataQuantityError: Raised if the data quantity is 0 and is weekday.
        """
        start_date = datetime.now(pytz.utc) - timedelta(days=1)
        if start_date.weekday() >= 5:
            return

        for k, v in data.items():
            if len(v) == 0:
                raise DataQuantityError(f"Data quantity for {k} is 0")
