"""SQLite storage for tasks, notes, and reminders."""

import os
import sqlite3
from datetime import datetime, timezone

from drico_bot.core.security import SECRET_FILE_MODE, secure_mkdir
from drico_bot.knowledge.pack import get_drico_home

CURRENT_SCHEMA_VERSION = 1
MAX_TASK_NOTE_LEN = 5000


def _db_path():
    return get_drico_home() / "drico.db"


def connect():
    secure_mkdir(str(get_drico_home()))
    path = _db_path()
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    try:
        os.chmod(str(path), SECRET_FILE_MODE)
    except OSError:
        pass
    return conn


def _utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def init_db(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS task_dependencies (
            task_id INTEGER NOT NULL,
            depends_on INTEGER NOT NULL,
            PRIMARY KEY (task_id, depends_on)
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_hhmm TEXT NOT NULL,
            text TEXT NOT NULL,
            fired INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    row = conn.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
    if row is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (CURRENT_SCHEMA_VERSION,))
    conn.commit()


def ensure_db():
    try:
        conn = connect()
        init_db(conn)
        conn.close()
    except sqlite3.DatabaseError:
        print("Drico > Warning: database corrupt. Starting fresh.")
        path = _db_path()
        if path.is_file():
            path.unlink()
        conn = connect()
        init_db(conn)
        conn.close()


def validate_text(text, label="text"):
    if text is None or not str(text).strip():
        raise ValueError("{0} cannot be empty.".format(label))
    text = str(text).strip()
    if len(text) > MAX_TASK_NOTE_LEN:
        raise ValueError("{0} exceeds {1} characters.".format(label, MAX_TASK_NOTE_LEN))
    if "\x00" in text:
        raise ValueError("NUL bytes are not allowed.")
    return text
