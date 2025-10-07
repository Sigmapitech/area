from importlib import import_module

from fastapi import APIRouter

from . import auth, graph, hello

optional_providers = ["spotify.spotify"]

loaded_modules = [auth, graph, hello]

for name in optional_providers:
    try:
        mod = import_module(f"...providers.{name}", package=__package__)
        loaded_modules.append(mod)
    except Exception as e:
        print(f"[WARN] Skipping provider '{name}' due to import error: {e}")

routers = []

for mod in loaded_modules:
    assert hasattr(
        mod, "router"
    ), f"Module {mod.__name__} is missing 'router' attribute"
    assert isinstance(
        mod.router, APIRouter
    ), f"'router' in module {mod.__name__} is not an APIRouter instance"
    print(
        f"Registering router from module: {mod.__name__} with prefix: {mod.router.prefix}"
    )
    routers.append(mod.router)


__all__ = ("routers",)
