from typing import Any, Callable


class Service:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.actions: list[dict[str, Any]] = []
        self.reactions: list[dict[str, Any]] = []

    def action(self, name: str, description: str):
        """Decorator to register an action with metadata."""
        def wrapper(func: Callable):
            self.actions.append({
                "name": name,
                "description": description,
                "function": func,
            })
            return func
        return wrapper

    def reaction(self, name: str, description: str):
        """Decorator to register a reaction with metadata."""
        def wrapper(func: Callable):
            self.reactions.append({
                "name": name,
                "description": description,
                "function": func,
            })
            return func
        return wrapper

    def to_dict(self) -> dict[str, Any]:
        """Serialize service info for JSON output (excluding function refs)."""
        return {
            "name": self.name,
            "description": self.description,
            "actions": [
                {"name": a["name"], "description": a["description"]}
                for a in self.actions
            ],
            "reactions": [
                {"name": r["name"], "description": r["description"]}
                for r in self.reactions
            ],
        }
