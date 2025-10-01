from fastapi import APIRouter

from . import auth, graph, hello

routers = []

for mod in (auth, graph, hello):
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
