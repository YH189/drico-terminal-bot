"""Tasks, notes, focus, reminders, brief, backup (Phase 4)."""

import csv
import io
import os
import shutil
import sqlite3
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

from drico_bot.core.registry import Command
from drico_bot.core.security import SECRET_FILE_MODE, secure_mkdir
from drico_bot.knowledge.pack import get_drico_home
from drico_bot.storage.database import connect, ensure_db, init_db, validate_text


def _task_add(context):
    raw = context.raw
    if not raw.startswith("task add "):
        return
    body = raw[len("task add ") :].strip()
    after_id = None
    if " --after " in body:
        body, dep = body.split(" --after ", 1)
        after_id = int(dep.strip())
    text = validate_text(body, "Task")
    conn = connect()
    init_db(conn)
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
    conn.commit()
    conn.close()
    print("Drico > Task {0} added.\n".format(task_id))


def _task_list(context):
    conn = connect()
    init_db(conn)
    rows = conn.execute("SELECT id, text, done FROM tasks ORDER BY id").fetchall()
    conn.close()
    if not rows:
        print("Drico > No tasks.\n")
        return
    for row in rows:
        status = "done" if row["done"] else "open"
        print("  {0} [{1}] {2}".format(row["id"], status, row["text"]))
    print()


def _task_done(context):
    parts = context.normalized.split()
    if len(parts) != 3:
        return
    task_id = int(parts[2])
    conn = connect()
    init_db(conn)
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Drico > Task {0} marked done.\n".format(task_id))


def _task_delete(context):
    parts = context.normalized.split()
    if len(parts) != 3:
        return
    task_id = int(parts[2])
    conn = connect()
    init_db(conn)
    conn.execute("DELETE FROM task_dependencies WHERE task_id = ? OR depends_on = ?", (task_id, task_id))
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Drico > Task {0} deleted.\n".format(task_id))


def _has_cycle(conn, task_id, depends_on):
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
        stack.extend(row[0] for row in rows)
    return False


def _note_add(context):
    text = validate_text(context.raw[len("note add ") :], "Note")
    conn = connect()
    init_db(conn)
    cur = conn.execute("INSERT INTO notes (text, created_at) VALUES (?, datetime('now'))", (text,))
    conn.commit()
    conn.close()
    print("Drico > Note {0} added.\n".format(cur.lastrowid))


def register(registry):
    ensure_db()
    registry.register(Command(name="task add", handler=_task_add, help_text="Add a task.", category="productivity"))
    registry.register(Command(name="task list", handler=_task_list, help_text="List tasks.", category="productivity"))
    registry.register(Command(name="task done", handler=_task_done, help_text="Mark task done.", category="productivity"))
    registry.register(Command(name="task delete", handler=_task_delete, help_text="Delete a task.", category="productivity", destructive=True))
    registry.register(Command(name="note add", handler=_note_add, help_text="Add a note.", category="productivity"))
    registry.register(Command(name="note list", handler=lambda c: _note_list(c), help_text="List notes.", category="productivity"))


def _note_list(context):
    conn = connect()
    init_db(conn)
    rows = conn.execute("SELECT id, text FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    for row in rows:
        print("  {0}: {1}".format(row["id"], row["text"]))
    print()
