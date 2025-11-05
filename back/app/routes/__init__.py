import importlib

from fastapi import APIRouter

routers = []
providers = (
    "about",
    "auth",
    "hello",
    "workflow",
    "spotify",
    "discord",
    "gmail",
    "caldav",
    "youtube",
    "oauth_base",
)

for mod_name in providers:
    try:
        mod = importlib.import_module(f".{mod_name}", __package__)

        assert hasattr(
            mod, "router"
        ), f"Module {mod.__name__} is missing 'router' attribute"
        assert isinstance(
            mod.router, APIRouter
        ), f"'router' in module {mod.__name__} is not an APIRouter instance"
        print(
            "Registering router from module:"
            f" {mod.__name__} with prefix: {mod.router.prefix}"
        )
        routers.append(mod.router)
    except Exception as e:
        print(e)

__all__ = ("routers",)
