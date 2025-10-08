import logging
from importlib import import_module

from fastapi import APIRouter

logger = logging.getLogger(__name__)

providers = ["spotify"]
loaded_modules = []


for name in providers:
    try:
        mod = import_module(f".{name}", package=__package__)
        loaded_modules.append(mod)
    except Exception as e:
        logger.warning(f"Skipping provider '{name}' due to import error: {e}")

routers = []

for mod in loaded_modules:
    assert hasattr(
        mod, "router"
    ), f"Module {mod.__name__} is missing 'router' attribute"
    assert isinstance(
        mod.router, APIRouter
    ), f"'router' in module {mod.__name__} is not an APIRouter instance"
    logger.info(
        f"Registering router from module: {mod.__name__} with prefix: {mod.router.prefix}"
    )
    routers.append(mod.router)


__all__ = ("routers",)
