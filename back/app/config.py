import os
import tomllib
from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError

CONFIG_PATH = os.getenv("AREA_CONFIG_PATH", "config.toml")


T = TypeVar("T", bound=BaseModel)


def fire_once(func):
    sentined = object()
    stored = sentined

    def wrapped(*args, **kwargs):
        nonlocal stored

        if stored is not sentined:
            return stored

        stored = func(*args, **kwargs)
        return stored

    return wrapped


@fire_once
def get_config() -> dict[str, Any]:
    assert os.path.exists(CONFIG_PATH), f"{CONFIG_PATH} does not exist."

    print(CONFIG_PATH)
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    return config


def get_package_config(package_name: str | None, type_: Type[T]) -> T:
    """
    Get configuration for a specific package and validate it against a Pydantic model.
    Args:
        package_name: The name of the package to get the configuration for.
        type_: A Pydantic model class to validate the configuration against.
    Returns:
        An instance of the Pydantic model with the configuration data.
    """
    assert issubclass(type_, BaseModel)
    assert package_name is not None

    package_layers: list[str] = package_name.removeprefix("app.").split(".")
    cfg = get_config()

    for pkg in package_layers:
        cfg = cfg.get(pkg, {})

    return type_(**cfg)
