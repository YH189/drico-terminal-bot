"""Security helpers (stdlib only)."""

import os
import stat

MAX_INPUT_LENGTH = 1000
DATA_DIR_MODE = 0o700
SECRET_FILE_MODE = 0o600


def normalize_and_limit(text):
    if text is None:
        return ""
    if "\x00" in text:
        raise ValueError("Input cannot contain NUL bytes.")
    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError(
            "Input is too long ({0} chars). Maximum is {1}.".format(
                len(text), MAX_INPUT_LENGTH
            )
        )
    return text


def secure_mkdir(path):
    path = os.path.abspath(path)
    os.makedirs(path, mode=DATA_DIR_MODE, exist_ok=True)
    _ensure_mode(path, DATA_DIR_MODE, is_dir=True)
    return path


def secure_write_file(path, content, mode=SECRET_FILE_MODE):
    path = os.path.abspath(path)
    parent = os.path.dirname(path)
    if parent:
        secure_mkdir(parent)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
    try:
        os.chmod(path, mode)
    except OSError:
        pass
    _warn_if_loose(path, mode)


def _ensure_mode(path, expected, is_dir=False):
    try:
        os.chmod(path, expected)
    except OSError:
        pass
    _warn_if_loose(path, expected, is_dir)


def _warn_if_loose(path, expected, is_dir=False):
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if mode != expected:
        kind = "directory" if is_dir else "file"
        print(
            "Drico > Warning: {0} {1} permissions are {2:o}, expected {3:o}.".format(
                kind, path, mode, expected
            )
        )


def warn_data_permissions(home):
    if not home:
        return
    path = os.path.abspath(home)
    if os.path.isdir(path):
        _warn_if_loose(path, DATA_DIR_MODE, is_dir=True)
