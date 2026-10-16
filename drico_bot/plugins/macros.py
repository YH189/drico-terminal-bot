"""Macro recording, list/run/delete."""

import json
import re
from pathlib import Path

from drico_bot.core.confirm import confirm
from drico_bot.core.dispatcher import Dispatcher
from drico_bot.core.registry import Command
from drico_bot.core.security import SECRET_FILE_MODE, secure_mkdir, secure_write_file
from drico_bot.knowledge.pack import get_drico_home
from drico_bot.storage.database import connect, ensure_db, init_db

MACRO_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")
STATE_RECORDING = "macro_recording"
STATE_COMMANDS = "macro_recording_commands"
CAPTURE_PRIORITY = 5


class MacroError(Exception):
    """User-facing macro error."""


def macros_dir():
    path = get_drico_home() / "macros"
    secure_mkdir(str(path))
    return path


def _conn():
    ensure_db()
    conn = connect()
    init_db(conn)
    return conn


def _state_get(conn, key):
    row = conn.execute("SELECT value FROM app_state WHERE key = ?", (key,)).fetchone()
    if row is None:
        return None
    return row["value"]


def _state_set(conn, key, value):
    conn.execute(
        "INSERT INTO app_state (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def _state_clear(conn, key):
    conn.execute("DELETE FROM app_state WHERE key = ?", (key,))


def validate_macro_name(name):
    if name is None or not str(name).strip():
        raise MacroError("Macro name cannot be empty.")
    name = str(name).strip()
    if not MACRO_NAME_RE.match(name):
        raise MacroError("Invalid macro name: {0}".format(name))
    return name


def macro_path(name):
    name = validate_macro_name(name)
    root = macros_dir().resolve()
    path = (root / "{0}.json".format(name)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        raise MacroError("Invalid macro name.")
    return path


def is_recording():
    conn = _conn()
    name = _state_get(conn, STATE_RECORDING)
    conn.close()
    return bool(name)


def recording_name():
    conn = _conn()
    name = _state_get(conn, STATE_RECORDING)
    conn.close()
    return name


def _load_buffer(conn):
    raw = _state_get(conn, STATE_COMMANDS)
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except (TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    return [str(item) for item in data if str(item).strip()]


def _save_buffer(conn, commands):
    _state_set(conn, STATE_COMMANDS, json.dumps(commands))


def record_start(name):
    name = validate_macro_name(name)
    conn = _conn()
    current = _state_get(conn, STATE_RECORDING)
    if current:
        conn.close()
        raise MacroError("Already recording macro '{0}'.".format(current))
    _state_set(conn, STATE_RECORDING, name)
    _save_buffer(conn, [])
    conn.commit()
    conn.close()
    return "Recording macro '{0}'. Type 'record stop' when done.".format(name)


def record_stop():
    conn = _conn()
    name = _state_get(conn, STATE_RECORDING)
    if not name:
        conn.close()
        raise MacroError("Not recording a macro.")
    commands = _load_buffer(conn)
    path = macro_path(name)
    payload = {"name": name, "commands": commands}
    secure_write_file(path, json.dumps(payload, indent=2) + "\n", mode=SECRET_FILE_MODE)
    _state_clear(conn, STATE_RECORDING)
    _state_clear(conn, STATE_COMMANDS)
    conn.commit()
    conn.close()
    return "Saved macro '{0}' ({1} commands).".format(name, len(commands))


def append_recorded_command(raw):
    conn = _conn()
    if not _state_get(conn, STATE_RECORDING):
        conn.close()
        return
    commands = _load_buffer(conn)
    commands.append(raw)
    _save_buffer(conn, commands)
    conn.commit()
    conn.close()


def macro_list():
    root = macros_dir()
    names = []
    for path in sorted(root.glob("*.json")):
        names.append(path.stem)
    if not names:
        return "No macros saved."
    lines = ["Macros:"]
    for name in names:
        lines.append("  {0}".format(name))
    return "\n".join(lines)


def load_macro(name):
    path = macro_path(name)
    if not path.is_file():
        raise MacroError("Macro not found: {0}".format(name))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        raise MacroError("Macro file is invalid: {0}".format(name))
    commands = data.get("commands") if isinstance(data, dict) else None
    if not isinstance(commands, list):
        raise MacroError("Macro file is invalid: {0}".format(name))
    return [str(item) for item in commands if str(item).strip()]


def macro_delete(name):
    name = validate_macro_name(name)
    path = macro_path(name)
    if not path.is_file():
        raise MacroError("Macro not found: {0}".format(name))
    path.unlink()
    return "Deleted macro '{0}'.".format(name)


def _redispatch(raw, normalized, session, registry):
    context_type = __import__("drico_bot.core.dispatcher", fromlist=["DispatchContext"]).DispatchContext
    context = context_type(raw=raw, normalized=normalized, session=session)
    command = registry.find(normalized)
    if command is not None and command.handler is not _recording_capture_handler:
        command.handler(context)
        return
    for command in registry.pattern_commands():
        if command.handler is _recording_capture_handler:
            continue
        if command.match_fn is not None and command.match_fn(context):
            command.handler(context)
            return
    Dispatcher.default_handler(context)


def macro_run(name, registry, session, normalize_fn):
    commands = load_macro(name)
    if not commands:
        return "Macro '{0}' has no commands.".format(name)
    for raw in commands:
        normalized = normalize_fn(raw)
        _redispatch(raw, normalized, session, registry)
    return "Ran macro '{0}' ({1} commands).".format(name, len(commands))


def _recording_capture_match(context):
    if not is_recording():
        return False
    norm = context.normalized
    if norm == "record stop" or norm.startswith("record stop "):
        return False
    if norm.startswith("record start"):
        return False
    return True


def _recording_capture_handler(context):
    append_recorded_command(context.raw)
    _redispatch(context.raw, context.normalized, context.session, context.session.registry)


def _handle_record_start(context):
    name = context.raw[len("record start ") :].strip()
    if not name:
        print("Drico > Usage: record start <name>\n")
        return
    try:
        message = record_start(name)
        print("Drico > {0}\n".format(message))
    except MacroError as exc:
        print("Drico > {0}\n".format(exc))


def _handle_record_stop(context):
    try:
        message = record_stop()
        print("Drico > {0}\n".format(message))
    except MacroError as exc:
        print("Drico > {0}\n".format(exc))


def _handle_macro_list(context):
    print("Drico > {0}\n".format(macro_list()))


def _handle_macro_run(context):
    name = context.raw[len("macro run ") :].strip()
    if not name:
        print("Drico > Usage: macro run <name>\n")
        return
    try:
        from drico_bot.core.text import normalize_text

        message = macro_run(name, context.session.registry, context.session, normalize_text)
        print("Drico > {0}\n".format(message))
    except MacroError as exc:
        print("Drico > {0}\n".format(exc))


def _handle_macro_delete(context):
    name = context.raw[len("macro delete ") :].strip()
    if not name:
        print("Drico > Usage: macro delete <name>\n")
        return
    try:
        validate_macro_name(name)
        path = macro_path(name)
        if not path.is_file():
            raise MacroError("Macro not found: {0}".format(name))
        if not confirm("Delete macro '{0}'? [y/N] ".format(name)):
            print("Drico > Cancelled.\n")
            return
        print("Drico > {0}\n".format(macro_delete(name)))
    except MacroError as exc:
        print("Drico > {0}\n".format(exc))


def register(registry):
    category = "macros"
    registry.register(
        Command(
            name="record start",
            handler=_handle_record_start,
            help_text="Start recording commands into a macro.",
            category=category,
        )
    )
    registry.register(
        Command(
            name="record stop",
            handler=_handle_record_stop,
            help_text="Stop recording and save the macro.",
            category=category,
        )
    )
    registry.register(
        Command(
            name="macro list",
            handler=_handle_macro_list,
            help_text="List saved macros.",
            category=category,
        )
    )
    registry.register(
        Command(
            name="macro run",
            handler=_handle_macro_run,
            help_text="Run a saved macro.",
            category=category,
        )
    )
    registry.register(
        Command(
            name="macro delete",
            handler=_handle_macro_delete,
            help_text="Delete a saved macro.",
            category=category,
            destructive=True,
        )
    )
    registry.register(
        Command(
            name="macro recording capture",
            handler=_recording_capture_handler,
            help_text="",
            category=category,
            match_fn=_recording_capture_match,
            priority=CAPTURE_PRIORITY,
            show_in_help=False,
        )
    )
