"""Interactive input with optional readline history (Phase 10)."""

import os
from pathlib import Path

_readline = None
try:
    import readline as _readline
except ImportError:
    pass


def read_line(prompt):
    hist_path = None
    home = os.environ.get("DRICO_HOME")
    if home and _readline is not None:
        hist_path = Path(home) / "history.txt"
        try:
            _readline.read_history_file(str(hist_path))
        except OSError:
            pass
    line = input(prompt)
    if hist_path is not None and _readline is not None:
        try:
            hist_path.parent.mkdir(parents=True, exist_ok=True)
            _readline.write_history_file(str(hist_path))
        except OSError:
            pass
    return line
