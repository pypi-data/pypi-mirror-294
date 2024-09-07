import json
from typing import Any
import requests
from bs_monitoring.alert_services.base import AlertService, register_alert_service
from bs_monitoring.common.utils import ConfigField


@register_alert_service
class OpsgenieAlertService(AlertService):
    api_key = ConfigField(str)

    def __init__(self, config: Any):
        """Alert service that sends alerts to Opsgenie.

        Args:
            args (OpsgenieAlertServiceConfig): The configuration for the alert service.
        """
        super().__init__(config)

    def build_alert(
        self,
        message: str,
        description: str | None = None,
        alias: str | None = None,
    ) -> dict[str, Any]:
        """Builds an alert object.

        Args:
            message (str): The message for the alert.
            description (Optional[str], optional): Description for the alert. Defaults to None.
            alias (Optional[str], optional): Alias for the alert. Defaults to None.

        Returns:
            Dict[str, Any]: The alert object.
        """
        return {
            "message": message,
            "description": description,
            "alias": alias,
        }

    def send_alert(
        self,
        message: str,
        description: str | None = None,
    ):
        """Sends an alert to the alert service.

        Args:
            message (str): Alert message
            description (Optional[str], optional): Alert description. Defaults to None.
            alias (Optional[str], optional): Alert alias. Defaults to None.

        Raises:
            Exception: Raised if the alert could not be sent.
        """
        body = self.build_alert(message, description)
        body = {k: v for k, v in body.items() if v is not None}

        url = "https://api.opsgenie.com/v2/alerts"
        headers = {
            "Authorization": f"GenieKey {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(url=url, headers=headers, data=json.dumps(body))
        if response.status_code != 202:
            raise Exception(f"Failed to send alert: {response.text}")
