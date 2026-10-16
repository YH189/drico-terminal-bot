"""Drico terminal entry point."""

import sys

from drico_bot.core.bootstrap import build_registry, run_cli
from drico_bot.core.dispatcher import Dispatcher, InteractiveSession
from drico_bot.core.text import normalize_text
from drico_bot.core.ui import show_banner


def run():
    if len(sys.argv) > 1:
        sys.exit(run_cli(sys.argv[1:]))

    registry = build_registry()
    session = InteractiveSession()
    session.registry = registry
    dispatcher = Dispatcher(registry)

    show_banner()

    while session.running:
        raw_user = input("User  > ").strip()

        if not raw_user:
            continue

        normalized = normalize_text(raw_user)
        dispatcher.dispatch(raw_user, normalized, session)


if __name__ == "__main__":
    run()
