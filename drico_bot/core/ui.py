import os
import sys
import time

from drico_bot.core.theme import style


def show_loading(message="Searching"):
    print(style("Drico > {0}".format(message), "accent"), end="", flush=True)

    if os.environ.get("DRICO_NO_DELAY") or not sys.stdout.isatty():
        print()
        return

    for _ in range(3):
        time.sleep(0.2)
        print(".", end="", flush=True)

    print()


def show_banner():
    bar = style("-" * 50, "banner")
    title = style("        DRICO - AI TOOLS ROUTER", "banner")
    print(bar)
    print(title)
    print(bar)
    print("Type 'show' to see the available commands.")
    print("Type 'exit' to close the program.\n")


def user_prompt():
    return style("User  > ", "prompt")
