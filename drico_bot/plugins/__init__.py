"""Minimal plugin registration for Drico CLI commands."""


class PluginRegistry:
    def __init__(self):
        self._commands = {}

    def register(self, name, handler, help_text=""):
        self._commands[name] = {"handler": handler, "help": help_text}

    def get(self, name):
        entry = self._commands.get(name)
        if entry is None:
            return None
        return entry["handler"]

    def names(self):
        return sorted(self._commands.keys())

    def help_lines(self):
        lines = []
        for name in self.names():
            lines.append("  {0}  {1}".format(name, self._commands[name]["help"]))
        return lines


def create_registry():
    registry = PluginRegistry()
    from drico_bot.plugins.knowledge import register as register_knowledge

    register_knowledge(registry)
    return registry
