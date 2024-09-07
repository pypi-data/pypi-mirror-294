from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from typing import Any
from dataclasses import dataclass
import pytz
from bs_monitoring.alert_services import alert, AlertService
from bs_monitoring.common.utils import ConfigField
from bs_monitoring.data_sources import DataSource, register_data_source


@dataclass
class ElasticDataSourceConfig:
    """Configuration for the Elasticsearch data source.

    Args:
        url (str): The URL for the Elasticsearch instance.
        indices (List[str]): The indices to consume messages from.
        basic_auth (Optional[List[str]], optional): Basic authentication credentials. Defaults to None.
        api_key (Optional[str], optional): API key for the Elasticsearch instance. Defaults to None.
        history_length (int, optional): The history length to consume messages from. Defaults to 1
    """

    url: str
    indices: list[str]
    basic_auth: list[str] | None = None
    api_key: str | None = None
    history_length: int = 1


@register_data_source
class ElasticDataSource(DataSource):
    basic_auth = ConfigField(list[str] | None, default=None)
    url = ConfigField(str)
    indices = ConfigField(list[str])
    api_key = ConfigField(str | None, default=None)
    history_length = ConfigField(int, default=1)

    def __init__(self, alert_service: AlertService, config: Any):
        """A data source that consumes messages from Elasticsearch.

        Args:
            args (ElasticDataSourceConfig): The configuration for the data source.
            alert_service (AlertService): The alert service to use.
        """
        super().__init__(config)
        auth = (
            {"basic_auth": tuple(self.basic_auth)}
            if self.basic_auth
            else {"api_key": self.api_key}
        )
        self.client_ = Elasticsearch(self.url, **auth)
        self.indices = self.indices
        self.history_length_ = self.history_length
        self.alert_service = alert_service

        self._setup()

    def _setup(self) -> None:
        """Set up the query for the Elasticsearch indices."""
        end = datetime.now(pytz.utc)
        start = end - timedelta(days=self.history_length_)

        end_ms = int(end.timestamp() * 1000)
        start_ms = int(start.timestamp() * 1000)
        self.query_ = {
            "query": {"range": {"@timestamp": {"gte": start_ms, "lte": end_ms}}},
            "sort": [{"@timestamp": {"order": "desc"}}],
        }

    @alert(
        message="Failed to consume messages from Elasticsearch.",
    )
    def produce(self) -> dict[str, list[dict[str, Any]]]:
        """Consumes messages from the Elasticsearch indices.

        Returns:
            Dict[str, List[Dict]]: A dictionary containing the consumed messages for each index.
        """
        events = {}
        for topic in self.indices:
            resp = self.client_.search(index=topic, body=self.query_)

            hits = list(map(lambda x: x["_source"], resp["hits"]["hits"]))
            events[topic] = hits

        return events
