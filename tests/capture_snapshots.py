"""Capture interactive command output for snapshot tests."""
import io
import os
import sys
import tempfile
from contextlib import redirect_stdout
from unittest import mock

import drico_bot.main as main


SESSION = [
    ("hi", "hi"),
    ("show", "show"),
    ("list", "list"),
    ("tool Claude", "tool Claude"),
    ("search tools code", "search tools code"),
    ("git status", "git status"),
    ("what is ai", "what is ai"),
    ("12+13", "12+13"),
    ("build", "build"),
    ("exit", "exit"),
    ("unknown text", "unknown text"),
]


def run_command(raw_input, drico_home):
    buf = io.StringIO()
    with redirect_stdout(buf):
        with mock.patch("sys.argv", ["drico-bot"]):
            with mock.patch.dict(os.environ, {"DRICO_HOME": drico_home}, clear=False):
                with mock.patch("builtins.input", side_effect=[raw_input, "exit"]):
                    with mock.patch("time.sleep", return_value=None):
                        with mock.patch.object(sys.stdout, "isatty", return_value=True):
                            main.run()
    return buf.getvalue()


def main_capture():
    drico_home = tempfile.mkdtemp(prefix="drico-snap-")
    for label, raw in SESSION:
        out = run_command(raw, drico_home)
        path = "tests/snapshots/{0}.txt".format(label.replace(" ", "_"))
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(out)


if __name__ == "__main__":
    main_capture()
