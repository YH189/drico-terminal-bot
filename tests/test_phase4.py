import io
import os
import zipfile
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

from drico_bot.core.dispatcher import Dispatcher, InteractiveSession
from drico_bot.core.registry import Registry
from drico_bot.plugins import productivity
from drico_bot.plugins.productivity import (
    _csv_escape_cell,
    _csv_unescape_cell,
    _dependency_graph_has_cycle,
    _safe_zip_target,
    check_reminders,
    register,
)
from drico_bot.storage.database import connect, ensure_db, init_db, validate_text


def _registry():
    reg = Registry()
    register(reg)
    return reg


def _dispatch(raw, registry, confirm_yes=False, confirm_no=False):
    session = InteractiveSession()
    session.registry = registry
    dispatcher = Dispatcher(registry)
    normalized = raw.lower().strip()
    patches = []
    if confirm_yes:
        patches.append(mock.patch("drico_bot.plugins.productivity.confirm", return_value=True))
    if confirm_no:
        patches.append(mock.patch("drico_bot.plugins.productivity.confirm", return_value=False))
    for patcher in patches:
        patcher.start()
    try:
        dispatcher.dispatch(raw, normalized, session)
    finally:
        for patcher in reversed(patches):
            patcher.stop()


def test_validate_text_rejects_empty():
    with pytest.raises(ValueError):
        validate_text("  ", "Task")


def test_task_crud_and_next(drico_home):
    ensure_db()
    reg = _registry()
    _dispatch("task add first", reg)
    _dispatch("task add second --after 1", reg)
    _dispatch("task list", reg)
    _dispatch("task next", reg)
    _dispatch("task done 1", reg)
    _dispatch("task next", reg)
    conn = connect()
    open_tasks = conn.execute("SELECT COUNT(*) AS c FROM tasks WHERE done = 0").fetchone()["c"]
    conn.close()
    assert open_tasks == 1


def test_task_cycle_blocked(drico_home, capsys):
    ensure_db()
    reg = _registry()
    _dispatch("task add a", reg)
    _dispatch("task add b --after 1", reg)
    _dispatch("task add c --after 2", reg)
    conn = connect()
    init_db(conn)
    conn.execute(
        "INSERT INTO task_dependencies (task_id, depends_on) VALUES (2, 3)"
    )
    conn.commit()
    assert _dependency_graph_has_cycle(conn) is True
    conn.close()
    _dispatch("task add blocked --after 1", reg)
    out = capsys.readouterr().out
    assert "cycle" in out.lower()
    _dispatch("task blocked", reg)


def test_note_search_delete(drico_home):
    ensure_db()
    reg = _registry()
    _dispatch("note add alpha note", reg)
    _dispatch("note add beta", reg)
    _dispatch("note search alpha", reg)
    _dispatch("note delete 1", reg, confirm_yes=True)


def test_focus_bounds(drico_home, capsys):
    ensure_db()
    reg = _registry()
    _dispatch("focus 0", reg)
    out = capsys.readouterr().out
    assert "between 1 and 240" in out
    _dispatch("focus 30", reg)
    conn = connect()
    row = conn.execute("SELECT value FROM app_state WHERE key = 'focus_until'").fetchone()
    conn.close()
    assert row is not None


def test_reminder_fires(drico_home, capsys):
    ensure_db()
    hhmm = datetime.now().strftime("%H:%M")
    reg = _registry()
    _dispatch("remind {0} ping".format(hhmm), reg)
    check_reminders()
    out = capsys.readouterr().out
    assert "ping" in out


def test_csv_formula_escape():
    assert _csv_escape_cell("=1+1").startswith("'")
    assert _csv_unescape_cell("'=1+1") == "=1+1"


def test_export_import_roundtrip(drico_home, tmp_path):
    ensure_db()
    reg = _registry()
    _dispatch("task add export me", reg)
    export_path = Path(drico_home) / "exports" / "tasks.csv"
    _dispatch("export tasks csv exports/tasks.csv", reg)
    assert export_path.is_file()
    content = export_path.read_text(encoding="utf-8")
    assert "export me" in content
    _dispatch("import tasks csv exports/tasks.csv", reg, confirm_yes=True)
    conn = connect()
    count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
    conn.close()
    assert count == 2


def test_backup_restore(drico_home):
    ensure_db()
    reg = _registry()
    _dispatch("task add backed", reg)
    _dispatch("backup", reg)
    backups = list((Path(drico_home) / "backups").glob("*.zip"))
    assert backups
    conn = connect()
    conn.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    archive = backups[0].name
    _dispatch("restore backups/{0}".format(archive), reg, confirm_yes=True)
    conn = connect()
    row = conn.execute("SELECT text FROM tasks").fetchone()
    conn.close()
    assert row is not None


def test_restore_rejects_zip_slip(drico_home, capsys):
    ensure_db()
    reg = _registry()
    evil = Path(drico_home) / "evil.zip"
    with zipfile.ZipFile(evil, "w") as zf:
        zf.writestr("../outside.txt", "nope")
    _dispatch("restore evil.zip", reg, confirm_yes=True)
    out = capsys.readouterr().out
    assert "failed" in out.lower() or "escapes" in out.lower()
    assert not (Path(drico_home).parent / "outside.txt").exists()


def test_safe_zip_target_rejects_escape(drico_home):
    root = Path(drico_home)
    with pytest.raises(ValueError):
        _safe_zip_target(root, "../escape")


def test_schedule_crontab_argv(drico_home):
    ensure_db()
    reg = _registry()
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(list(argv))
        if argv[0] == "crontab" and argv[1] == "-l":
            return mock.Mock(returncode=0, stdout="", stderr="")
        return mock.Mock(returncode=0, stdout="", stderr="")

    with mock.patch("drico_bot.plugins.productivity.subprocess.run", side_effect=fake_run):
        _dispatch("schedule add 0 9 * * * echo hello", reg)
    assert ["crontab", "-"] in calls
    write_call = [c for c in calls if c == ["crontab", "-"]]
    assert write_call


def test_schedule_list_and_remove(drico_home):
    ensure_db()
    reg = _registry()
    sample = "0 9 * * * echo hi {0} abc123\n".format(productivity.DRICO_CRON_MARKER)

    def fake_run(argv, **kwargs):
        if argv[0] == "crontab" and argv[1] == "-l":
            return mock.Mock(returncode=0, stdout=sample, stderr="")
        return mock.Mock(returncode=0, stdout="", stderr="")

    with mock.patch("drico_bot.plugins.productivity.subprocess.run", side_effect=fake_run):
        _dispatch("schedule list", reg)
        _dispatch("schedule remove abc123", reg, confirm_yes=True)


def test_new_template_scaffold(drico_home, tmp_path, monkeypatch):
    ensure_db()
    monkeypatch.chdir(tmp_path)
    reg = _registry()
    _dispatch("new python-cli demo", reg)
    assert (tmp_path / "demo" / "main.py").is_file()


def test_brief_output(drico_home, capsys):
    ensure_db()
    reg = _registry()
    _dispatch("task add one", reg)
    _dispatch("brief", reg)
    out = capsys.readouterr().out
    assert "Brief" in out
    assert "Open tasks" in out


def test_task_delete_cancel(drico_home, capsys):
    ensure_db()
    reg = _registry()
    _dispatch("task add keep", reg)
    _dispatch("task delete 1", reg, confirm_no=True)
    conn = connect()
    count = conn.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
    conn.close()
    assert count == 1
