import os
import stat
from unittest import mock

import pytest

from drico_bot.core.config import _validate_config, ensure_drico_home, load_config
from drico_bot.core.dispatcher import Dispatcher
from drico_bot.core.plugin_loader import load_builtin_plugins
from drico_bot.core.registry import Registry
from drico_bot.core.security import MAX_INPUT_LENGTH, normalize_and_limit


def test_input_length_limit():
    with pytest.raises(ValueError):
        normalize_and_limit("x" * (MAX_INPUT_LENGTH + 1))


def test_broken_plugin_isolated(tmp_path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "broken.py").write_text(
        "def register(registry):\n    raise RuntimeError('boom')\n",
        encoding="utf-8",
    )
    registry = Registry()
    load_builtin_plugins(registry, {}, plugins_dir=plugins_dir)
    assert any(p.name == "broken" and p.status == "error" for p in registry.plugin_statuses())


def test_invalid_config_falls_back():
    out = _validate_config({"disabled": "not-a-table"})
    assert out["disabled"]["plugins"] == []


def test_data_directory_mode_0700(drico_home, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", drico_home)
    path = ensure_drico_home()
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert mode == 0o700


def test_dispatcher_catches_handler_errors():
    registry = Registry()

    def boom(_ctx):
        raise RuntimeError("fail")

    from drico_bot.core.registry import Command

    registry.register(Command(name="boom", handler=boom, help_text=""))
    dispatcher = Dispatcher(registry)
    session = mock.Mock()
    with mock.patch("builtins.print") as printed:
        dispatcher.dispatch("boom", "boom", session)
    assert any("Error" in str(c) for c in printed.call_args_list)
