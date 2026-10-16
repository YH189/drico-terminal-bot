from drico_bot.builtin_data import CONCEPT_ALIASES, CONCEPTS
from drico_bot.builtin_data import TOOLS
from drico_bot.plugins.references import find_reference, find_reference_command
from drico_bot.plugins.tools import find_category
from drico_bot.builtin_data import REFERENCES
import io
import sys
from contextlib import redirect_stdout
from unittest import mock

import drico_bot.main as main
from drico_bot.core.ui import show_loading


def test_llms_alias_maps_to_llm():
    assert CONCEPT_ALIASES["large language models"] == "llm"
    assert "llms" not in CONCEPTS


def test_reference_word_boundary_not_domain():
    assert find_reference("c domain") is None or find_reference_command(
        "c domain", REFERENCES.get("c", {})
    ) is None
    assert find_reference_command("c main", REFERENCES["c"]) == "main"
    assert find_reference_command("c domain", REFERENCES["c"]) is None


def test_tool_count():
    buf = io.StringIO()
    total = sum(len(v) for v in TOOLS.values())
    with redirect_stdout(buf):
        with mock.patch("sys.argv", ["drico-bot"]):
            with mock.patch.dict("os.environ", {"DRICO_HOME": "/tmp/drico-p2"}, clear=False):
                with mock.patch("builtins.input", side_effect=["tool count", "exit"]):
                    with mock.patch("time.sleep", return_value=None):
                        with mock.patch.object(sys.stdout, "isatty", return_value=True):
                            main.run()
    assert "Total tools: {0}".format(total) in buf.getvalue()


def test_show_lists_registry_categories(drico_home):
    buf = io.StringIO()
    with redirect_stdout(buf):
        with mock.patch("sys.argv", ["drico-bot"]):
            with mock.patch.dict("os.environ", {"DRICO_HOME": drico_home}, clear=False):
                with mock.patch("builtins.input", side_effect=["show", "exit"]):
                    with mock.patch("time.sleep", return_value=None):
                        with mock.patch.object(sys.stdout, "isatty", return_value=True):
                            main.run()
    out = buf.getvalue()
    assert "[basics]" in out
    assert "[tools]" in out


def test_loading_delay_skipped_with_env():
    buf = io.StringIO()
    with redirect_stdout(buf):
        with mock.patch.dict("os.environ", {"DRICO_NO_DELAY": "1"}, clear=False):
            with mock.patch("time.sleep") as sleep:
                show_loading("Searching")
                sleep.assert_not_called()
    assert "Searching\n" in buf.getvalue()


def test_loading_delay_skipped_non_tty():
    buf = io.StringIO()
    with redirect_stdout(buf):
        with mock.patch.object(sys.stdout, "isatty", return_value=False):
            with mock.patch("time.sleep") as sleep:
                show_loading("Searching")
                sleep.assert_not_called()
