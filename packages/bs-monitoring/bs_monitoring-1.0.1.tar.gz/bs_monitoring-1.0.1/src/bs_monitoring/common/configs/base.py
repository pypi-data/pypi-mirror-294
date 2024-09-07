import yaml
import os
import re
from dataclasses import dataclass, field
from typing import Any
from dacite import from_dict, Config
from argparse import ArgumentParser, ArgumentTypeError

from bs_monitoring.alert_services import AlertServiceConfig
from bs_monitoring.monitors import MonitorConfig
from bs_monitoring.data_sources import DataSourceConfig
from bs_monitoring.databases import DatabaseConfig
# from bs_monitoring.common.utils import import_submodules


@dataclass
class RootConfig:
    """Configuration for the service, contains configurations for the different components.
    Is read from a YAML file.

    Args:
        DataSource (DataSourceConfig): The configuration for the data source component.
        AlertService (AlertServiceConfig): The configuration for the alert service component.
        Monitors (List[MonitorConfig]): The configuration for the monitor components.
    """

    DataSource: DataSourceConfig
    AlertService: AlertServiceConfig
    Monitors: list[MonitorConfig]
    Databases: list[DatabaseConfig] = field(default_factory=list)


def read_yaml_config(file_path: str) -> RootConfig:
    """Reads a YAML configuration file and returns a RootConfig object.

    Args:
        file_path (str): The path to the YAML configuration file.

    Raises:
        ArgumentTypeError: Raised if the file cannot be read or the configuration is invalid.

    Returns:
        RootConfig: The configuration object.
    """

    def replace_env_vars(value: Any):
        if isinstance(value, str):
            return re.sub(
                r"\$\{([^}^{]+)\}",
                lambda x: os.environ.get(x.group(1), x.group(0)),
                value,
            )
        elif isinstance(value, dict):
            return {k: replace_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_env_vars(v) for v in value]
        return value

    # import_submodules("monitors")
    # import_submodules("alert_services")
    # import_submodules("data_sources")
    # import_submodules("databases")

    with open(file_path, "r") as file:
        try:
            dct = replace_env_vars(yaml.safe_load(file))

            config = from_dict(
                data_class=RootConfig, data=dct, config=Config(strict=True)
            )
            return config
        except yaml.YAMLError as e:
            raise ArgumentTypeError(f"Error parsing YAML file: {e}")
        except Exception as e:
            raise ArgumentTypeError(f"Error parsing configuration: {e}")


def read_config() -> RootConfig:
    """Parses the command line arguments and reads the configuration file.

    Returns:
        RootConfig: The configuration object.
    """
    parser = ArgumentParser(
        description="Service monitoring quality and quantity of messages from Kafka."
    )
    parser.add_argument(
        "--config",
        type=read_yaml_config,
        help="The path to the configuration file.",
        required=True,
    )
    return parser.parse_args().config
