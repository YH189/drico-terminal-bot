"""Command registry with longest-match lookup."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class Command:
    name: str
    aliases: Tuple[str, ...] = ()
    handler: Callable = None
    help_text: str = ""
    category: str = "general"
    match_fn: Optional[Callable] = None
    priority: int = 100
    destructive: bool = False
    show_in_help: bool = True


@dataclass
class PluginStatus:
    name: str
    status: str


class Registry:
    def __init__(self):
        self._commands: List[Command] = []
        self._cli: Dict[str, Dict[str, Any]] = {}
        self._plugins: List[PluginStatus] = []

    def register(self, name, handler=None, help_text="", **kwargs):
        """Register an interactive Command or a CLI handler (knowledge CLI API)."""
        if isinstance(name, Command):
            self._commands.append(name)
            return
        if kwargs.get("cli_only"):
            self._cli[name] = {"handler": handler, "help": help_text}
            return
        command = Command(
            name=name,
            aliases=tuple(kwargs.get("aliases", ())),
            handler=handler,
            help_text=help_text,
            category=kwargs.get("category", "general"),
            match_fn=kwargs.get("match_fn"),
            priority=kwargs.get("priority", 100),
            destructive=kwargs.get("destructive", False),
            show_in_help=kwargs.get("show_in_help", True),
        )
        self._commands.append(command)

    def help_by_category(self):
        grouped = {}
        for command in self._commands:
            if not command.show_in_help:
                continue
            names = [command.name]
            names.extend(command.aliases)
            label = " / ".join(names)
            grouped.setdefault(command.category, []).append((label, command.help_text))
        return grouped

    def register_cli(self, name, handler, help_text=""):
        self._cli[name] = {"handler": handler, "help": help_text}

    def get_cli(self, name):
        entry = self._cli.get(name)
        if entry is None:
            return None
        return entry["handler"]

    def record_plugin(self, name, status):
        self._plugins.append(PluginStatus(name=name, status=status))

    def plugin_statuses(self):
        return list(self._plugins)

    def all(self):
        return list(self._commands)

    def pattern_commands(self):
        matched = [cmd for cmd in self._commands if cmd.match_fn is not None]
        return sorted(matched, key=lambda item: item.priority)

    def _all_keys(self):
        keys = []
        for command in self._commands:
            if command.match_fn is not None:
                continue
            keys.append((command.name, command))
            for alias in command.aliases:
                keys.append((alias, command))
        return keys

    def find(self, normalized_text):
        if not normalized_text:
            return None
        best = None
        best_len = -1
        for key, command in self._all_keys():
            if normalized_text == key:
                if len(key) > best_len:
                    best = command
                    best_len = len(key)
            elif normalized_text.startswith(key + " "):
                if len(key) > best_len:
                    best = command
                    best_len = len(key)
        return best
