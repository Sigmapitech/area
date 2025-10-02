from . import graph, hello, auth

routers = [mod.router for mod in (hello, auth, graph)]

__all__ = ("routers",)
