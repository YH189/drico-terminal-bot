import json
import os
from unittest import mock

import pytest

from drico_bot.core.dispatcher import Dispatcher, InteractiveSession
from drico_bot.core.registry import Registry
from drico_bot.core.text import normalize_text
from drico_bot.plugins.macros import (
    MacroError,
    append_recorded_command,
    is_recording,
    macro_path,
    macro_run,
    record_start,
    record_stop,
    register as register_macros,
)
from drico_bot.plugins.runner import (
    RunnerError,
    append_run_log,
    mask_log_text,
    mask_secret_value,
    read_run_logs,
    register as register_runner,
    run_argv,
    run_log_path,
)
from drico_bot.storage.database import ensure_db


def _registry():
    reg = Registry()
    register_macros(reg)
    register_runner(reg)
    return reg


def _dispatch(raw, registry, confirm_yes=False, confirm_no=False):
    session = InteractiveSession()
    session.registry = registry
    dispatcher = Dispatcher(registry)
    patches = []
    if confirm_yes:
        patches.append(mock.patch("drico_bot.plugins.macros.confirm", return_value=True))
    if confirm_no:
        patches.append(mock.patch("drico_bot.plugins.macros.confirm", return_value=False))
    for patcher in patches:
        patcher.start()
    try:
        dispatcher.dispatch(raw, normalize_text(raw), session)
    finally:
        for patcher in reversed(patches):
            patcher.stop()


def test_mask_secret_value():
    assert mask_secret_value("abcd") == "abcd"
    assert mask_secret_value("secretvalue") == "secr***"


def test_mask_log_text_masks_assignment():
    line = "run echo password=supersecret"
    masked = mask_log_text(line)
    assert "supersecret" not in masked
    assert "supe***" in masked


def test_run_whitelist_rejects_unknown():
    with pytest.raises(RunnerError, match="whitelist"):
        run_argv(["rm", "-rf", "/"])


def test_run_echo_and_log(drico_home):
    result = run_argv(["echo", "hello"])
    assert result.returncode == 0
    assert "hello" in result.stdout
    assert run_log_path().is_file()
    lines = read_run_logs()
    assert lines
    assert "echo" in lines[-1]


def test_run_env_allowlist(drico_home, monkeypatch):
    monkeypatch.setenv("SECRET_TOKEN", "must-not-leak")
    monkeypatch.setenv("PATH", os.environ.get("PATH", "/usr/bin"))
    captured = {}

    def fake_run(argv, cwd=None, capture_output=True, text=True, env=None, shell=False):
        captured["env"] = env
        return mock.Mock(returncode=0, stdout="ok\n", stderr="")

    with mock.patch("drico_bot.plugins.runner.subprocess.run", side_effect=fake_run):
        run_argv(["echo", "x"])
    assert "SECRET_TOKEN" not in (captured.get("env") or {})


def test_record_start_stop_saves_macro(drico_home):
    ensure_db()
    record_start("demo")
    assert is_recording()
    append_recorded_command("echo one")
    append_recorded_command("echo two")
    message = record_stop()
    assert "2 commands" in message
    path = macro_path("demo")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["commands"] == ["echo one", "echo two"]


def test_record_start_twice_raises(drico_home):
    ensure_db()
    record_start("a")
    with pytest.raises(MacroError, match="Already recording"):
        record_start("b")


def test_macro_list_run_delete(drico_home, capsys):
    ensure_db()
    reg = _registry()
    _dispatch("record start work", reg)
    _dispatch("run echo hi", reg)
    _dispatch("record stop", reg)
    _dispatch("macro list", reg)
    out = capsys.readouterr().out
    assert "work" in out
    _dispatch("macro run work", reg)
    out = capsys.readouterr().out
    assert "hi" in out
    _dispatch("macro delete work", reg, confirm_no=True)
    out = capsys.readouterr().out
    assert "Cancelled" in out
    _dispatch("macro delete work", reg, confirm_yes=True)
    out = capsys.readouterr().out
    assert "Deleted" in out
    with pytest.raises(MacroError):
        macro_run("work", reg, InteractiveSession(), normalize_text)


def test_logs_command(drico_home, capsys):
    append_run_log(["echo", "test"], 0)
    reg = _registry()
    _dispatch("logs 5", reg)
    out = capsys.readouterr().out
    assert "echo" in out
