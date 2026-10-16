"""Route normalized user input to registered command handlers."""

from dataclasses import dataclass

from drico_bot.core.registry import Registry


@dataclass
class DispatchContext:
    raw: str
    normalized: str
    session: object


class InteractiveSession:
    def __init__(self):
        self.running = True


class Dispatcher:
    def __init__(self, registry):
        self.registry = registry

    def dispatch(self, raw, normalized, session):
        context = DispatchContext(raw=raw, normalized=normalized, session=session)

        command = self.registry.find(normalized)
        if command is not None:
            command.handler(context)
            return

        for command in self.registry.pattern_commands():
            if command.match_fn(context):
                command.handler(context)
                return

        self.default_handler(context)

    @staticmethod
    def default_handler(context):
        print("Drico > I don't understand that yet.")
        print("Drico > Type 'show' to see what I can do.\n")
