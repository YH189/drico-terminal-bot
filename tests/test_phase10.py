import os
from unittest import mock

from drico_bot.core.theme import colors_enabled, style
from drico_bot.core.ui import show_banner


def test_no_color_disables_styles():
    with mock.patch.dict(os.environ, {"NO_COLOR": "1"}, clear=False):
        assert colors_enabled() is False
        assert style("hello", "accent") == "hello"


def test_plain_theme_disables_styles(monkeypatch):
    monkeypatch.setattr(
        "drico_bot.core.theme.load_config",
        lambda: {"ui": {"theme": "plain"}},
    )
    assert colors_enabled() is False


def test_default_theme_adds_ansi_when_enabled(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr(
        "drico_bot.core.theme.load_config",
        lambda: {"ui": {"theme": "default"}},
    )
    text = style("x", "prompt")
    assert text.startswith("\033[")
    assert text.endswith("x\033[0m") or "x" in text


def test_show_banner_no_color_plain_output(capsys, monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    show_banner()
    out = capsys.readouterr().out
    assert "\033[" not in out
    assert "DRICO" in out


def test_notify_uses_notify_send_when_available():
    from drico_bot.core.notify import notify

    with mock.patch("drico_bot.core.notify.shutil.which", return_value="/usr/bin/notify-send"):
        with mock.patch("drico_bot.core.notify.subprocess.run") as run:
            assert notify("t", "b") is True
            run.assert_called_once()
            assert run.call_args[0][0][0] == "notify-send"
