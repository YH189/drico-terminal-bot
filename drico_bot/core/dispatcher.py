"""Route normalized user input to registered command handlers."""

import os
import traceback
from dataclasses import dataclass

from drico_bot.core.registry import Registry
from drico_bot.core.security import normalize_and_limit
from drico_bot.core.text import normalize_text


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

    def prepare_input(self, raw):
        raw = normalize_and_limit(raw.strip())
        normalized = normalize_text(raw)
        return raw, normalized

    def dispatch(self, raw, normalized, session):
        context = DispatchContext(raw=raw, normalized=normalized, session=session)

        try:
            command = self.registry.find(normalized)
            if command is not None:
                self._run_handler(command.handler, context)
                return

            for command in self.registry.pattern_commands():
                if command.match_fn(context):
                    self._run_handler(command.handler, context)
                    return

            self.default_handler(context)
        except ValueError as exc:
            print("Drico > {0}\n".format(exc))

    @staticmethod
    def _run_handler(handler, context):
        try:
            handler(context)
        except Exception as exc:
            if os.environ.get("DRICO_DEBUG") == "1":
                traceback.print_exc()
            else:
                print("Drico > Error: {0}\n".format(exc))

    @staticmethod
    def default_handler(context):
        print("Drico > I don't understand that yet.")
        print("Drico > Type 'show' to see what I can do.\n")
