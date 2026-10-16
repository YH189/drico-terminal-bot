"""Tasks, notes, focus, reminders, brief, backup, export, schedule, templates (Phase 4)."""

import csv
import io
import os
import re
import shutil
import sqlite3
import subprocess
import uuid
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

from drico_bot.core.confirm import confirm
from drico_bot.core.paths import safe_path_under
from drico_bot.core.registry import Command
from drico_bot.core.security import SECRET_FILE_MODE, secure_mkdir
from drico_bot.knowledge.pack import get_drico_home
from drico_bot.storage.database import connect, ensure_db, init_db, validate_text

DRICO_CRON_MARKER = "# drico:"
FOCUS_MIN_MINUTES = 1
FOCUS_MAX_MINUTES = 240
TEMPLATE_NAMES = ("python-cli", "python-package", "fastapi-basic")
BACKUP_FILES = ("drico.db", "config.toml")


def _conn():
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


def _has_cycle(conn, task_id, depends_on):
    if task_id == depends_on:
        return True
    stack = [depends_on]
    seen = set()
    while stack:
        current = stack.pop()
        if current == task_id:
            return True
        if current in seen:
            continue
        seen.add(current)
        rows = conn.execute(
            "SELECT depends_on FROM task_dependencies WHERE task_id = ?", (current,)
        ).fetchall()
        stack.extend(row["depends_on"] for row in rows)
    return False


def _dependency_graph_has_cycle(conn):
    rows = conn.execute("SELECT task_id, depends_on FROM task_dependencies").fetchall()
    graph = {}
    nodes = set()
    for row in rows:
        graph.setdefault(row["task_id"], []).append(row["depends_on"])
        nodes.add(row["task_id"])
        nodes.add(row["depends_on"])

    def visit(node, path):
        if node in path:
            return True
        path.add(node)
        for dep in graph.get(node, []):
            if visit(dep, path):
                return True
        path.remove(node)
        return False

    for node in nodes:
        if visit(node, set()):
            return True
    return False


def _task_exists(conn, task_id):
    row = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return row is not None


def _open_task_ids(conn):
    rows = conn.execute("SELECT id FROM tasks WHERE done = 0 ORDER BY id").fetchall()
    return [row["id"] for row in rows]


def _blocked_ids(conn):
    blocked = set()
    for task_id in _open_task_ids(conn):
        deps = conn.execute(
            "SELECT depends_on FROM task_dependencies WHERE task_id = ?", (task_id,)
        ).fetchall()
        for dep in deps:
            row = conn.execute(
                "SELECT done FROM tasks WHERE id = ?", (dep["depends_on"],)
            ).fetchone()
            if row is None or not row["done"]:
                blocked.add(task_id)
                break
    return blocked


def _next_task_id(conn):
    blocked = _blocked_ids(conn)
    for task_id in _open_task_ids(conn):
        if task_id not in blocked:
            return task_id
    return None


def _parse_task_id(parts, index=2):
    if len(parts) <= index:
        raise ValueError("Missing task id.")
    try:
        return int(parts[index])
    except ValueError:
        raise ValueError("Invalid task id.")


def _task_add(context):
    raw = context.raw
    if not raw.startswith("task add "):
        return
    body = raw[len("task add ") :].strip()
    after_id = None
    if " --after " in body:
        body, dep = body.split(" --after ", 1)
        try:
            after_id = int(dep.strip())
        except ValueError:
            print("Drico > Invalid --after task id.\n")
            return
    try:
        text = validate_text(body, "Task")
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    conn = _conn()
    if after_id is not None and not _task_exists(conn, after_id):
        conn.close()
        print("Drico > Dependency task {0} does not exist.\n".format(after_id))
        return
    cur = conn.execute(
        "INSERT INTO tasks (text, done, created_at) VALUES (?, 0, datetime('now'))",
        (text,),
    )
    task_id = cur.lastrowid
    if after_id is not None:
        conn.execute(
            "INSERT INTO task_dependencies (task_id, depends_on) VALUES (?, ?)",
            (task_id, after_id),
        )
        if _dependency_graph_has_cycle(conn):
            conn.execute(
                "DELETE FROM task_dependencies WHERE task_id = ? AND depends_on = ?",
                (task_id, after_id),
            )
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            print("Drico > Cannot add dependency: cycle detected.\n")
            return
    conn.commit()
    conn.close()
    print("Drico > Task {0} added.\n".format(task_id))


def _task_list(context):
    conn = _conn()
    rows = conn.execute("SELECT id, text, done FROM tasks ORDER BY id").fetchall()
    blocked = _blocked_ids(conn)
    conn.close()
    if not rows:
        print("Drico > No tasks.\n")
        return
    for row in rows:
        status = "done" if row["done"] else "open"
        suffix = ""
        if not row["done"] and row["id"] in blocked:
            suffix = " (blocked)"
        print("  {0} [{1}]{2} {3}".format(row["id"], status, suffix, row["text"]))
    print()


def _task_done(context):
    parts = context.normalized.split()
    try:
        task_id = _parse_task_id(parts)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    conn = _conn()
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Drico > Task {0} marked done.\n".format(task_id))


def _task_delete(context):
    parts = context.normalized.split()
    try:
        task_id = _parse_task_id(parts)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if not confirm("Delete task {0}? [y/N] ".format(task_id)):
        print("Drico > Cancelled.\n")
        return
    conn = _conn()
    conn.execute(
        "DELETE FROM task_dependencies WHERE task_id = ? OR depends_on = ?",
        (task_id, task_id),
    )
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Drico > Task {0} deleted.\n".format(task_id))


def _task_blocked(context):
    conn = _conn()
    blocked = sorted(_blocked_ids(conn))
    if not blocked:
        conn.close()
        print("Drico > No blocked tasks.\n")
        return
    for task_id in blocked:
        row = conn.execute("SELECT text FROM tasks WHERE id = ?", (task_id,)).fetchone()
        text = row["text"] if row else ""
        print("  {0}: {1}".format(task_id, text))
    conn.close()
    print()


def _task_next(context):
    conn = _conn()
    task_id = _next_task_id(conn)
    if task_id is None:
        conn.close()
        print("Drico > No available tasks.\n")
        return
    row = conn.execute("SELECT text FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    print("Drico > Next: {0} — {1}\n".format(task_id, row["text"]))


def _note_add(context):
    try:
        text = validate_text(context.raw[len("note add ") :], "Note")
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    conn = _conn()
    cur = conn.execute(
        "INSERT INTO notes (text, created_at) VALUES (?, datetime('now'))", (text,)
    )
    note_id = cur.lastrowid
    conn.commit()
    conn.close()
    print("Drico > Note {0} added.\n".format(note_id))


def _note_list(context):
    conn = _conn()
    rows = conn.execute("SELECT id, text FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    if not rows:
        print("Drico > No notes.\n")
        return
    for row in rows:
        print("  {0}: {1}".format(row["id"], row["text"]))
    print()


def _note_search(context):
    query = context.raw[len("note search ") :].strip()
    if not query:
        print("Drico > Usage: note search <text>\n")
        return
    if len(query) > 200:
        print("Drico > Search query too long (max 200).\n")
        return
    conn = _conn()
    rows = conn.execute(
        "SELECT id, text FROM notes WHERE text LIKE ? ORDER BY id DESC",
        ("%{0}%".format(query.replace("%", "").replace("_", "")),),
    ).fetchall()
    conn.close()
    if not rows:
        print("Drico > No matching notes.\n")
        return
    for row in rows:
        print("  {0}: {1}".format(row["id"], row["text"]))
    print()


def _note_delete(context):
    parts = context.normalized.split()
    try:
        note_id = _parse_task_id(parts)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if not confirm("Delete note {0}? [y/N] ".format(note_id)):
        print("Drico > Cancelled.\n")
        return
    conn = _conn()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    print("Drico > Note {0} deleted.\n".format(note_id))


def _parse_focus_minutes(parts):
    if len(parts) != 2:
        raise ValueError("Usage: focus <1-240>")
    try:
        minutes = int(parts[1])
    except ValueError:
        raise ValueError("Invalid minutes.")
    if minutes < FOCUS_MIN_MINUTES or minutes > FOCUS_MAX_MINUTES:
        raise ValueError("Focus minutes must be between {0} and {1}.".format(
            FOCUS_MIN_MINUTES, FOCUS_MAX_MINUTES
        ))
    return minutes


def _handle_focus(context):
    parts = context.normalized.split()
    try:
        minutes = _parse_focus_minutes(parts)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    ends = datetime.now() + timedelta(minutes=minutes)
    conn = _conn()
    _state_set(conn, "focus_until", ends.isoformat(timespec="seconds"))
    conn.commit()
    conn.close()
    print(
        "Drico > Focus for {0} min (until {1}).\n".format(
            minutes, ends.strftime("%H:%M")
        )
    )


def _parse_hhmm(text):
    match = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", text.strip())
    if not match:
        raise ValueError("Invalid time. Use HH:MM (24h).")
    hour = int(match.group(1))
    minute = int(match.group(2))
    return "{0:02d}:{1:02d}".format(hour, minute)


def _handle_remind(context):
    body = context.raw[len("remind ") :].strip()
    parts = body.split(None, 1)
    if len(parts) < 2:
        print("Drico > Usage: remind HH:MM <text>\n")
        return
    try:
        hhmm = _parse_hhmm(parts[0])
        text = validate_text(parts[1], "Reminder")
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    conn = _conn()
    cur = conn.execute(
        "INSERT INTO reminders (time_hhmm, text, fired) VALUES (?, ?, 0)",
        (hhmm, text),
    )
    rid = cur.lastrowid
    conn.commit()
    conn.close()
    print("Drico > Reminder {0} set for {1}.\n".format(rid, hhmm))


def check_reminders():
    now = datetime.now().strftime("%H:%M")
    conn = _conn()
    rows = conn.execute(
        "SELECT id, text FROM reminders WHERE time_hhmm = ? AND fired = 0", (now,)
    ).fetchall()
    for row in rows:
        print("Drico > Reminder: {0}".format(row["text"]))
        conn.execute("UPDATE reminders SET fired = 1 WHERE id = ?", (row["id"],))
    if rows:
        print()
    conn.commit()
    conn.close()


def _focus_remaining(conn):
    raw = _state_get(conn, "focus_until")
    if not raw:
        return None
    try:
        ends = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if ends <= datetime.now():
        _state_clear(conn, "focus_until")
        return None
    delta = ends - datetime.now()
    return int(delta.total_seconds() // 60) + 1


def _handle_brief(context):
    conn = _conn()
    open_count = conn.execute("SELECT COUNT(*) AS c FROM tasks WHERE done = 0").fetchone()["c"]
    note_count = conn.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    next_id = _next_task_id(conn)
    blocked = len(_blocked_ids(conn))
    focus_min = _focus_remaining(conn)
    pending = conn.execute(
        "SELECT COUNT(*) AS c FROM reminders WHERE fired = 0"
    ).fetchone()["c"]
    conn.commit()
    conn.close()
    print("Drico > Brief")
    print("  Open tasks: {0} (blocked: {1})".format(open_count, blocked))
    if next_id is not None:
        print("  Next task id: {0}".format(next_id))
    print("  Notes: {0}".format(note_count))
    print("  Pending reminders: {0}".format(pending))
    if focus_min is not None:
        print("  Focus: {0} min remaining".format(focus_min))
    print()


def _backups_dir():
    path = get_drico_home() / "backups"
    secure_mkdir(str(path))
    return path


def _safe_zip_target(root, member):
    root = Path(root).resolve()
    target = (root / member).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise ValueError("Zip entry escapes destination.")
    return target


def _handle_backup(context):
    home = get_drico_home()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = _backups_dir() / "drico-backup-{0}.zip".format(stamp)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in BACKUP_FILES:
            path = home / name
            if path.is_file():
                zf.write(path, arcname=name)
    try:
        os.chmod(str(dest), SECRET_FILE_MODE)
    except OSError:
        pass
    print("Drico > Backup written to {0}\n".format(dest))


def _handle_restore(context):
    parts = context.raw.split(None, 1)
    if len(parts) < 2:
        print("Drico > Usage: restore <backup.zip>\n")
        return
    try:
        archive = safe_path_under(get_drico_home(), parts[1].strip())
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if not archive.is_file():
        print("Drico > Backup file not found.\n")
        return
    if not confirm("Restore from {0}? This overwrites data. [y/N] ".format(archive.name)):
        print("Drico > Cancelled.\n")
        return
    home = get_drico_home()
    try:
        with zipfile.ZipFile(archive, "r") as zf:
            for member in zf.namelist():
                if member.endswith("/"):
                    continue
                target = _safe_zip_target(home, member)
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                if target.name == "drico.db":
                    try:
                        os.chmod(str(target), SECRET_FILE_MODE)
                    except OSError:
                        pass
    except (zipfile.BadZipFile, ValueError) as exc:
        print("Drico > Restore failed: {0}\n".format(exc))
        return
    print("Drico > Restore complete.\n")


def _csv_escape_cell(value):
    text = str(value)
    if text and text[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + text
    return text


def _csv_unescape_cell(value):
    if value and value[0] == "'" and len(value) > 1:
        return value[1:]
    return value


def _export_tasks_md(conn):
    rows = conn.execute(
        "SELECT id, text, done, created_at FROM tasks ORDER BY id"
    ).fetchall()
    lines = ["# Tasks", ""]
    for row in rows:
        status = "done" if row["done"] else "open"
        lines.append("## {0} [{1}]".format(row["id"], status))
        lines.append(row["text"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _export_notes_md(conn):
    rows = conn.execute(
        "SELECT id, text, created_at FROM notes ORDER BY id"
    ).fetchall()
    lines = ["# Notes", ""]
    for row in rows:
        lines.append("## {0}".format(row["id"]))
        lines.append(row["text"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _export_tasks_csv(conn):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "text", "done", "created_at"])
    rows = conn.execute(
        "SELECT id, text, done, created_at FROM tasks ORDER BY id"
    ).fetchall()
    for row in rows:
        writer.writerow([
            row["id"],
            _csv_escape_cell(row["text"]),
            row["done"],
            row["created_at"],
        ])
    return buf.getvalue()


def _export_notes_csv(conn):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "text", "created_at"])
    rows = conn.execute(
        "SELECT id, text, created_at FROM notes ORDER BY id"
    ).fetchall()
    for row in rows:
        writer.writerow([
            row["id"],
            _csv_escape_cell(row["text"]),
            row["created_at"],
        ])
    return buf.getvalue()


def _write_export(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)
    try:
        os.chmod(str(path), SECRET_FILE_MODE)
    except OSError:
        pass


def _handle_export(context):
    norm = context.normalized
    parts = norm.split()
    if len(parts) < 3:
        print("Drico > Usage: export tasks|notes md|csv [path]\n")
        return
    kind, fmt = parts[1], parts[2]
    if kind not in ("tasks", "notes") or fmt not in ("md", "csv"):
        print("Drico > Usage: export tasks|notes md|csv [path]\n")
        return
    tail = context.raw.split(None, 3)
    if len(tail) > 3:
        out_path = tail[3]
    else:
        out_path = str(get_drico_home() / "exports" / "{0}.{1}".format(kind, fmt))
    try:
        dest = safe_path_under(get_drico_home(), out_path)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    conn = _conn()
    if kind == "tasks" and fmt == "md":
        content = _export_tasks_md(conn)
    elif kind == "tasks" and fmt == "csv":
        content = _export_tasks_csv(conn)
    elif kind == "notes" and fmt == "md":
        content = _export_notes_md(conn)
    else:
        content = _export_notes_csv(conn)
    conn.close()
    _write_export(dest, content)
    print("Drico > Exported to {0}\n".format(dest))


def _import_tasks_csv(conn, path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = _csv_unescape_cell(row.get("text", "").strip())
            if not text:
                continue
            text = validate_text(text, "Task")
            done = 1 if str(row.get("done", "0")).strip() in ("1", "true", "yes") else 0
            conn.execute(
                "INSERT INTO tasks (text, done, created_at) VALUES (?, ?, datetime('now'))",
                (text, done),
            )


def _import_notes_csv(conn, path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = _csv_unescape_cell(row.get("text", "").strip())
            if not text:
                continue
            text = validate_text(text, "Note")
            conn.execute(
                "INSERT INTO notes (text, created_at) VALUES (?, datetime('now'))",
                (text,),
            )


def _import_tasks_md(conn, text):
    blocks = re.split(r"\n##\s+", text)
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        header = lines[0]
        body = "\n".join(lines[1:]).strip()
        if not body:
            continue
        m = re.match(r"^(\d+)\s+\[(done|open)\]", header)
        done = 1 if m and m.group(2) == "done" else 0
        body = validate_text(body, "Task")
        conn.execute(
            "INSERT INTO tasks (text, done, created_at) VALUES (?, ?, datetime('now'))",
            (body, done),
        )


def _import_notes_md(conn, text):
    blocks = re.split(r"\n##\s+", text)
    for block in blocks[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        if not body:
            body = lines[0]
        body = validate_text(body, "Note")
        conn.execute(
            "INSERT INTO notes (text, created_at) VALUES (?, datetime('now'))",
            (body,),
        )


def _handle_import(context):
    norm = context.normalized
    parts = norm.split()
    if len(parts) < 4:
        print("Drico > Usage: import tasks|notes md|csv <path>\n")
        return
    kind, fmt = parts[1], parts[2]
    if kind not in ("tasks", "notes") or fmt not in ("md", "csv"):
        print("Drico > Usage: import tasks|notes md|csv <path>\n")
        return
    file_part = context.raw.split(None, 3)
    if len(file_part) < 4:
        print("Drico > Usage: import tasks|notes md|csv <path>\n")
        return
    try:
        src = safe_path_under(get_drico_home(), file_part[3])
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if not src.is_file():
        print("Drico > Import file not found.\n")
        return
    if not confirm("Import {0} into {1}? [y/N] ".format(src.name, kind)):
        print("Drico > Cancelled.\n")
        return
    conn = _conn()
    try:
        if fmt == "csv":
            if kind == "tasks":
                _import_tasks_csv(conn, src)
            else:
                _import_notes_csv(conn, src)
        else:
            text = src.read_text(encoding="utf-8")
            if kind == "tasks":
                _import_tasks_md(conn, text)
            else:
                _import_notes_md(conn, text)
        conn.commit()
    except (ValueError, OSError, csv.Error) as exc:
        conn.rollback()
        conn.close()
        print("Drico > Import failed: {0}\n".format(exc))
        return
    conn.close()
    print("Drico > Import complete.\n")


def _read_crontab():
    result = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def _write_crontab(content):
    proc = subprocess.run(
        ["crontab", "-"],
        input=content,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "crontab failed")


def _parse_schedule_lines(text):
    entries = []
    for line in text.splitlines():
        if DRICO_CRON_MARKER not in line:
            continue
        marker_idx = line.index(DRICO_CRON_MARKER)
        schedule_id = line[marker_idx + len(DRICO_CRON_MARKER) :].strip()
        cron_part = line[:marker_idx].strip()
        entries.append((schedule_id, cron_part, line))
    return entries


def _handle_schedule_add(context):
    body = context.raw[len("schedule add ") :].strip()
    if not body:
        print("Drico > Usage: schedule add <cron> <command>\n")
        return
    parts = body.split()
    if len(parts) < 6:
        print("Drico > Usage: schedule add <cron> <command>\n")
        return
    cron = " ".join(parts[0:5])
    command = " ".join(parts[5:])
    schedule_id = uuid.uuid4().hex[:8]
    line = "{0} {1} {2} {3}\n".format(cron, command, DRICO_CRON_MARKER, schedule_id)
    existing = _read_crontab()
    if existing and not existing.endswith("\n"):
        existing += "\n"
    try:
        _write_crontab(existing + line)
    except RuntimeError as exc:
        print("Drico > {0}\n".format(exc))
        return
    print("Drico > Scheduled {0} (id {1}).\n".format(cron, schedule_id))


def _handle_schedule_list(context):
    entries = _parse_schedule_lines(_read_crontab())
    if not entries:
        print("Drico > No scheduled jobs.\n")
        return
    for schedule_id, cron_part, _line in entries:
        print("  {0}: {1}".format(schedule_id, cron_part))
    print()


def _handle_schedule_remove(context):
    parts = context.normalized.split()
    if len(parts) != 3:
        print("Drico > Usage: schedule remove <id>\n")
        return
    schedule_id = parts[2]
    if not confirm("Remove schedule {0}? [y/N] ".format(schedule_id)):
        print("Drico > Cancelled.\n")
        return
    existing = _read_crontab()
    kept = []
    removed = False
    for line in existing.splitlines():
        if DRICO_CRON_MARKER in line:
            sid = line.split(DRICO_CRON_MARKER, 1)[1].strip()
            if sid == schedule_id:
                removed = True
                continue
        kept.append(line)
    if not removed:
        print("Drico > Schedule id not found.\n")
        return
    new_text = "\n".join(kept)
    if new_text:
        new_text += "\n"
    try:
        _write_crontab(new_text)
    except RuntimeError as exc:
        print("Drico > {0}\n".format(exc))
        return
    print("Drico > Schedule {0} removed.\n".format(schedule_id))


def _templates_root():
    return Path(__file__).resolve().parent.parent / "templates"


def _handle_new(context):
    parts = context.normalized.split()
    if len(parts) != 3:
        print("Drico > Usage: new <template> <name>\n")
        return
    template, name = parts[1], parts[2]
    if template not in TEMPLATE_NAMES:
        print("Drico > Unknown template. Choose: {0}\n".format(", ".join(TEMPLATE_NAMES)))
        return
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        print("Drico > Invalid project name.\n")
        return
    src_root = _templates_root() / template
    if not src_root.is_dir():
        print("Drico > Template missing on disk.\n")
        return
    cwd = Path.cwd()
    try:
        dest = safe_path_under(cwd, name)
    except ValueError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if dest.exists():
        print("Drico > Target already exists.\n")
        return
    dest.mkdir(parents=True)
    for path in src_root.rglob("*"):
        rel = path.relative_to(src_root)
        target = dest / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    print("Drico > Created {0} from template {1}.\n".format(dest, template))


def register(registry):
    ensure_db()
    category = "productivity"
    commands = [
        ("task add", _task_add, "Add a task (optional --after <id>)."),
        ("task list", _task_list, "List tasks."),
        ("task done", _task_done, "Mark a task done."),
        ("task delete", _task_delete, "Delete a task.", True),
        ("task blocked", _task_blocked, "List blocked tasks."),
        ("task next", _task_next, "Show next available task."),
        ("note add", _note_add, "Add a note."),
        ("note list", _note_list, "List notes."),
        ("note search", _note_search, "Search notes."),
        ("note delete", _note_delete, "Delete a note.", True),
        ("focus", _handle_focus, "Focus timer (1-240 minutes)."),
        ("remind", _handle_remind, "Set a reminder at HH:MM."),
        ("brief", _handle_brief, "Productivity summary."),
        ("backup", _handle_backup, "Zip backup of local data."),
        ("restore", _handle_restore, "Restore from a backup zip.", True),
        ("export tasks md", lambda c: _handle_export(c), "Export tasks as Markdown."),
        ("export tasks csv", lambda c: _handle_export(c), "Export tasks as CSV."),
        ("export notes md", lambda c: _handle_export(c), "Export notes as Markdown."),
        ("export notes csv", lambda c: _handle_export(c), "Export notes as CSV."),
        ("import tasks md", _handle_import, "Import tasks from Markdown.", True),
        ("import tasks csv", _handle_import, "Import tasks from CSV.", True),
        ("import notes md", _handle_import, "Import notes from Markdown.", True),
        ("import notes csv", _handle_import, "Import notes from CSV.", True),
        ("schedule add", _handle_schedule_add, "Add a crontab entry."),
        ("schedule list", _handle_schedule_list, "List Drico crontab entries."),
        ("schedule remove", _handle_schedule_remove, "Remove a scheduled job.", True),
        ("new", _handle_new, "Scaffold from a template."),
    ]
    for name, handler, help_text, *rest in commands:
        destructive = bool(rest)
        registry.register(
            Command(
                name=name,
                handler=handler,
                help_text=help_text,
                category=category,
                destructive=destructive,
            )
        )
