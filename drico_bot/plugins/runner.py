"""Safe whitelisted subprocess runner with masked run logs."""

import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from drico_bot.core.registry import Command
from drico_bot.core.security import SECRET_FILE_MODE, secure_mkdir, secure_write_file
from drico_bot.knowledge.pack import get_drico_home

RUN_WHITELIST = frozenset(
    {
        "cat",
        "date",
        "echo",
        "find",
        "git",
        "grep",
        "head",
        "ls",
        "pwd",
        "python",
        "python3",
        "pytest",
        "sort",
        "tail",
        "true",
        "false",
        "uname",
        "wc",
        "which",
    }
)

ALLOWED_ENV_KEYS = frozenset(
    {
        "DRICO_HOME",
        "HOME",
        "LANG",
        "LC_ALL",
        "PATH",
        "PWD",
        "PYTHONPATH",
        "TERM",
        "USER",
        "VIRTUAL_ENV",
    }
)

LOG_MASK_PATTERNS = [
    re.compile(
        r"(?i)(api[_-]?key|secret|password|token|auth[_-]?token)"
        r"(\s*[=:]\s*)(\S+)"
    ),
    re.compile(r"(AKIA[0-9A-Z]{16})"),
]

MAX_LOG_BYTES = 512 * 1024
DEFAULT_LOG_LINES = 30
MAX_LOG_LINES = 200


class RunnerError(Exception):
    """User-facing runner error."""


def logs_dir():
    path = get_drico_home() / "logs"
    secure_mkdir(str(path))
    return path


def run_log_path():
    return logs_dir() / "run.log"


def mask_secret_value(value):
    text = str(value)
    if len(text) <= 4:
        return text
    return text[:4] + "***"


def mask_log_text(text):
    masked = text
    for pattern in LOG_MASK_PATTERNS:
        if pattern.pattern.startswith("(?i)(api"):
            masked = pattern.sub(
                lambda m: "{0}{1}{2}".format(m.group(1), m.group(2), mask_secret_value(m.group(3))),
                masked,
            )
        else:
            masked = pattern.sub(lambda m: mask_secret_value(m.group(1)), masked)
    return masked


def _filtered_env():
    env = {}
    for key in ALLOWED_ENV_KEYS:
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def run_argv(argv, cwd=None):
    if not argv:
        raise RunnerError("Usage: run <command> [args...]")
    program = argv[0]
    base = os.path.basename(program)
    if base not in RUN_WHITELIST:
        raise RunnerError("Command not in whitelist: {0}".format(base))
    if cwd is None:
        cwd = os.getcwd()
    result = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=_filtered_env(),
        shell=False,
    )
    append_run_log(argv, result.returncode)
    return result


def append_run_log(argv, returncode):
    line = "{0} exit={1}\n".format(" ".join(argv), returncode)
    line = mask_log_text(line)
    path = run_log_path()
    existing = ""
    if path.is_file():
        try:
            existing = path.read_text(encoding="utf-8")
        except OSError:
            existing = ""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = "[{0}] {1}".format(stamp, line)
    combined = existing + entry
    if len(combined.encode("utf-8")) > MAX_LOG_BYTES:
        combined = combined[-MAX_LOG_BYTES :]
    secure_write_file(str(path), combined, mode=SECRET_FILE_MODE)


def read_run_logs(limit=DEFAULT_LOG_LINES):
    limit = max(1, min(int(limit), MAX_LOG_LINES))
    path = run_log_path()
    if not path.is_file():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return lines[-limit:]


def _parse_run_argv(context):
    body = context.raw[len("run ") :].strip()
    if not body:
        raise RunnerError("Usage: run <command> [args...]")
    try:
        return shlex.split(body, posix=os.name != "nt")
    except ValueError as exc:
        raise RunnerError("Invalid run command: {0}".format(exc)) from exc


def _handle_run(context):
    try:
        argv = _parse_run_argv(context)
        result = run_argv(argv)
    except RunnerError as exc:
        print("Drico > {0}\n".format(exc))
        return
    if result.stdout:
        print(result.stdout.rstrip("\n"))
    if result.stderr:
        print(result.stderr.rstrip("\n"), file=sys.stderr)
    if result.returncode != 0:
        print("Drico > Exit code {0}\n".format(result.returncode))
    else:
        print()


def _handle_logs(context):
    parts = context.normalized.split()
    limit = DEFAULT_LOG_LINES
    if len(parts) >= 2:
        try:
            limit = int(parts[1])
        except ValueError:
            print("Drico > Usage: logs [lines]\n")
            return
    lines = read_run_logs(limit)
    if not lines:
        print("Drico > No run log entries yet.\n")
        return
    for line in lines:
        print(line)
    print()


def register(registry):
    category = "run"
    registry.register(
        Command(
            name="run",
            handler=_handle_run,
            help_text="Run a whitelisted command (argv only).",
            category=category,
        )
    )
    registry.register(
        Command(
            name="logs",
            handler=_handle_logs,
            help_text="Show recent masked run log lines.",
            category=category,
        )
    )
