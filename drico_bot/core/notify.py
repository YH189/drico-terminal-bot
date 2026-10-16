"""Optional desktop notifications via notify-send (Phase 10)."""

import shutil
import subprocess


def notify(title, body):
    """Send a desktop notification when notify-send is available."""
    if not shutil.which("notify-send"):
        return False
    subprocess.run(
        ["notify-send", title, body],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return True
