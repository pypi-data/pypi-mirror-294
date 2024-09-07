from typing import Any
from dataclasses import field, make_dataclass


class ConfigField:
    def __init__(self, field_type: type, default: Any = None):
        self.field_type = field_type
        self.default = default

    def _to_attribute(self) -> tuple[Any, Any] | Any:
        if self.default is not None:
            return (self.field_type, field(default=self.default))
        return (self.field_type,)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj.config, self.name)

    def __set__(self, obj, value):
        setattr(obj.config, self.name, value)


def register_config(cls: type, config_type: type):
    config_fields = [
        (name, *value._to_attribute())
        for name, value in vars(cls).items()
        if isinstance(value, ConfigField)
    ]
    c = make_dataclass(cls.__name__ + "Config", config_fields)
    setattr(cls, "config", c)
    if not config_type.__annotations__[
        "config"
    ]:  # DON'T TOUCH, DACITE BREAKS UNLESS THIS IS HERE
        config_type.__annotations__["config"] = c
    else:
        config_type.__annotations__["config"] |= c


class MonitoringServiceError(Exception):
    """Base class for exceptions in the monitoring service."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

