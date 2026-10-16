from drico_bot.storage.database import connect, init_db, validate_text
import pytest


def test_task_crud(drico_home, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", drico_home)
    from drico_bot.storage.database import ensure_db

    ensure_db()
    conn = connect()
    init_db(conn)
    conn.execute("INSERT INTO tasks (text, done, created_at) VALUES ('a', 0, 'now')")
    conn.commit()
    row = conn.execute("SELECT id FROM tasks").fetchone()
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (row["id"],))
    conn.commit()
    done = conn.execute("SELECT done FROM tasks WHERE id = ?", (row["id"],)).fetchone()
    assert done["done"] == 1
    conn.close()


def test_validate_text_rejects_empty():
    with pytest.raises(ValueError):
        validate_text("  ", "Task")
