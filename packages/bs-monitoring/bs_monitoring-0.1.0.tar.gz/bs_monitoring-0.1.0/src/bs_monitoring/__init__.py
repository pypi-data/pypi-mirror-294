import pkgutil
import importlib


def import_submodules(package_name: str) -> None:
    package = importlib.import_module(package_name)
    for _, name, _ in pkgutil.walk_packages(package.__path__):
        importlib.import_module(f"{package.__name__}.{name}")
