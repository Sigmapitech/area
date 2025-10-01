from . import auth, hello

routers = [mod.router for mod in (hello, auth)]

__all__ = ("routers",)
