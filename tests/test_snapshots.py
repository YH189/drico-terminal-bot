import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import drico_bot.main as main

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"

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


def _run_command(raw_input, drico_home):
    buf = io.StringIO()
    with redirect_stdout(buf):
        with mock.patch("sys.argv", ["drico-bot"]):
            with mock.patch.dict(
                "os.environ",
                {"DRICO_HOME": drico_home, "NO_COLOR": "1"},
                clear=False,
            ):
                with mock.patch("builtins.input", side_effect=[raw_input, "exit"]):
                    with mock.patch("time.sleep", return_value=None):
                        with mock.patch.object(sys.stdout, "isatty", return_value=True):
                            main.run()
    return buf.getvalue()


def test_interactive_snapshots_match_baseline(drico_home):
    for label, raw in SESSION:
        expected_path = SNAPSHOT_DIR / "{0}.txt".format(label.replace(" ", "_"))
        expected = expected_path.read_text(encoding="utf-8")
        actual = _run_command(raw, drico_home)
        assert actual == expected, "Snapshot mismatch for: {0}".format(label)
