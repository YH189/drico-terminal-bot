"""Poll a folder for mtime changes and re-index every interval (default 5s)."""

import os
import time
from pathlib import Path

from drico_bot.knowledge.folder_index import FolderIndexError, index_folder

DEFAULT_POLL_SECONDS = 5


def _folder_mtime_snapshot(root):
    root = Path(root).resolve()
    latest = 0.0
    for dirpath, _dirnames, filenames in os.walk(root, followlinks=False):
        for name in filenames:
            path = Path(dirpath) / name
            try:
                latest = max(latest, path.stat().st_mtime)
            except OSError:
                continue
    return latest


def watch_folder(
    folder_path,
    poll_seconds=DEFAULT_POLL_SECONDS,
    sleep_fn=time.sleep,
    should_continue=None,
):
    """
    Re-index folder when any file mtime increases. Stop when should_continue() is False
    or on KeyboardInterrupt.
    """
    root = Path(folder_path).resolve()
    if not root.is_dir():
        raise FolderIndexError("Not a directory: {0}".format(folder_path))

    if should_continue is None:
        should_continue = lambda: True

    last_mtime = _folder_mtime_snapshot(root)
    index_folder(root)
    print("Watching {0} (poll every {1}s). Press Ctrl+C to stop.".format(root, poll_seconds))

    try:
        while should_continue():
            sleep_fn(poll_seconds)
            if not should_continue():
                break
            current = _folder_mtime_snapshot(root)
            if current > last_mtime:
                index_folder(root)
                print("Re-indexed {0}.".format(root))
                last_mtime = current
    except KeyboardInterrupt:
        print("Watch stopped.")
        return 0
    return 0
