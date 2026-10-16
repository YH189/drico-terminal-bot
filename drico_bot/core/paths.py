"""Safe path resolution under an allowed root."""

from pathlib import Path


def safe_path_under(root, user_path):
    if user_path is None or "\x00" in str(user_path):
        raise ValueError("Invalid path.")
    root = Path(root).resolve()
    target = Path(user_path)
    if not target.is_absolute():
        target = (root / target).resolve()
    else:
        target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise ValueError("Path escapes the allowed directory.")
    return target
