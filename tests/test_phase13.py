import io
from unittest import mock

from drico_bot.core.doctor import run_doctor
from drico_bot.core.registry import Registry
from drico_bot.plugins.system import register


def test_doctor_reports_python(tmp_path, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    text = run_doctor()
    assert "Python:" in text
    assert str(tmp_path) in text


def test_setup_creates_plugins_dir(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    reg = Registry()
    register(reg)
    cmd = reg.find("setup")
    session = mock.Mock()
    session.registry = reg
    from drico_bot.core.dispatcher import DispatchContext

    ctx = DispatchContext(raw="setup", normalized="setup", session=session)
    cmd.handler(ctx)
    assert (tmp_path / "plugins").is_dir()


def test_reset_requires_delete_typed(tmp_path, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    (tmp_path / "marker.txt").write_text("x", encoding="utf-8")
    reg = Registry()
    register(reg)
    cmd = reg.find("reset")
    session = mock.Mock()
    session.registry = reg
    from drico_bot.core.dispatcher import DispatchContext

    ctx = DispatchContext(raw="reset --all", normalized="reset --all", session=session)
    with mock.patch("drico_bot.plugins.system.confirm_typed", return_value=False):
        cmd.handler(ctx)
    assert tmp_path.exists()
