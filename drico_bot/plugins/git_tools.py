"""Git tools: summary, hotspots, blame-summary, stale-branches, undo-last, hooks."""

import os
import subprocess
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from drico_bot.core.confirm import confirm
from drico_bot.core.registry import Command

HOOK_MARKER = "# drico-git-hooks"
HOOK_NAME = "pre-commit"
DEFAULT_STALE_DAYS = 30
DEFAULT_HOTSPOT_LIMIT = 15
DEFAULT_SUMMARY_COMMITS = 5
MAX_STALE_DAYS = 3650
MAX_HOTSPOT_LIMIT = 100
MAX_SUMMARY_COMMITS = 50


class GitToolsError(Exception):
    """User-facing git tools error."""


def _run_git(args, cwd=None, check=True):
    if cwd is None:
        cwd = Path.cwd()
    result = subprocess.run(
        ["git"] + list(args),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        message = (result.stderr or result.stdout or "git failed").strip()
        raise GitToolsError(message.splitlines()[0])
    return result


def git_root(cwd=None):
    if cwd is None:
        cwd = Path.cwd()
    result = _run_git(["rev-parse", "--show-toplevel"], cwd=cwd, check=False)
    if result.returncode != 0:
        raise GitToolsError("Not a git repository.")
    return Path(result.stdout.strip())


def _current_branch(cwd):
    result = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd, check=False)
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def _parse_positive_int(value, default, maximum, label):
    if value is None or not str(value).strip():
        return default
    try:
        number = int(str(value).strip())
    except ValueError:
        raise GitToolsError("Invalid {0}: {1}".format(label, value))
    if number < 1:
        raise GitToolsError("{0} must be at least 1.".format(label))
    if number > maximum:
        raise GitToolsError("{0} cannot exceed {1}.".format(label, maximum))
    return number


def git_summary(cwd=None, commit_count=None):
    root = git_root(cwd)
    count = _parse_positive_int(
        commit_count, DEFAULT_SUMMARY_COMMITS, MAX_SUMMARY_COMMITS, "commit count"
    )
    branch = _current_branch(root)
    lines = ["Git summary ({0})".format(root.name), "Branch: {0}".format(branch)]

    status = _run_git(["status", "--porcelain"], cwd=root, check=False)
    if status.returncode == 0:
        changed = [line for line in status.stdout.splitlines() if line.strip()]
        lines.append("Changed files: {0}".format(len(changed)))

    upstream = _run_git(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=root,
        check=False,
    )
    if upstream.returncode == 0 and upstream.stdout.strip():
        tracking = upstream.stdout.strip()
        ahead_behind = _run_git(
            ["rev-list", "--left-right", "--count", "HEAD...@{u}"],
            cwd=root,
            check=False,
        )
        if ahead_behind.returncode == 0:
            parts = ahead_behind.stdout.strip().split()
            if len(parts) == 2:
                lines.append(
                    "Tracking {0}: ahead {1}, behind {2}".format(
                        tracking, parts[0], parts[1]
                    )
                )

    log = _run_git(
        ["log", "-n", str(count), "--oneline", "--decorate"],
        cwd=root,
        check=False,
    )
    lines.append("Recent commits:")
    if log.returncode != 0 or not log.stdout.strip():
        lines.append("  (none)")
    else:
        for entry in log.stdout.splitlines():
            lines.append("  {0}".format(entry))
    return "\n".join(lines)


def hotspots_report(cwd=None, limit=None, path=None):
    root = git_root(cwd)
    max_items = _parse_positive_int(
        limit, DEFAULT_HOTSPOT_LIMIT, MAX_HOTSPOT_LIMIT, "limit"
    )
    args = ["log", "--pretty=format:", "--name-only"]
    if path:
        args.append("--")
        args.append(path)
    result = _run_git(args, cwd=root, check=False)
    if result.returncode != 0:
        raise GitToolsError((result.stderr or "git log failed").strip().splitlines()[0])

    counts = Counter()
    for line in result.stdout.splitlines():
        name = line.strip()
        if not name:
            continue
        counts[name] += 1

    lines = ["Change hotspots (by commit touches):"]
    if not counts:
        lines.append("No file history found.")
        return "\n".join(lines)

    for rel, touch_count in counts.most_common(max_items):
        lines.append("  {0}  {1}".format(touch_count, rel))
    if len(counts) > max_items:
        lines.append("  ... and {0} more files".format(len(counts) - max_items))
    return "\n".join(lines)


def blame_summary(path, cwd=None, limit=10):
    if not path or not str(path).strip():
        raise GitToolsError("Usage: blame-summary <file>")
    root = git_root(cwd)
    rel = str(path).strip()
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        raise GitToolsError("Path escapes the git repository.")

    result = _run_git(
        ["blame", "--line-porcelain", rel],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        message = (result.stderr or "git blame failed").strip().splitlines()
        raise GitToolsError(message[0] if message else "git blame failed.")

    authors = Counter()
    for line in result.stdout.splitlines():
        if line.startswith("author "):
            authors[line[7:]] += 1

    lines = ["Blame summary for {0}:".format(rel)]
    if not authors:
        lines.append("No blame data.")
        return "\n".join(lines)

    total = sum(authors.values())
    lines.append("Lines: {0}".format(total))
    for author, line_count in authors.most_common(limit):
        percent = int(round(100.0 * line_count / total))
        lines.append("  {0}  {1} ({2}%)".format(line_count, author, percent))
    return "\n".join(lines)


def stale_branches_report(cwd=None, days=None):
    root = git_root(cwd)
    stale_days = _parse_positive_int(
        days, DEFAULT_STALE_DAYS, MAX_STALE_DAYS, "days"
    )
    cutoff = datetime.utcnow() - timedelta(days=stale_days)
    result = _run_git(
        [
            "for-each-ref",
            "--sort=-committerdate",
            "refs/heads/",
            "--format=%(refname:short)\t%(committerdate:iso8601)",
        ],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise GitToolsError("Cannot list branches.")

    current = _current_branch(root)
    stale = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        name, date_text = parts[0].strip(), parts[1].strip()
        try:
            if date_text.endswith("Z"):
                date_text = date_text[:-1] + "+00:00"
            committed = datetime.fromisoformat(date_text)
            if committed.tzinfo is not None:
                committed = committed.replace(tzinfo=None)
        except ValueError:
            continue
        if committed <= cutoff:
            stale.append((name, date_text[:10]))

    lines = [
        "Stale branches (no commits in {0} days, excluding current):".format(
            stale_days
        )
    ]
    if not stale:
        lines.append("None.")
        return "\n".join(lines)

    for name, date_text in stale:
        if name == current:
            continue
        lines.append("  {0}  last commit {1}".format(name, date_text))
    if len(lines) == 1:
        lines.append("None.")
    return "\n".join(lines)


def undo_last_commit(cwd=None, stdin=None):
    root = git_root(cwd)
    count = _run_git(["rev-list", "--count", "HEAD"], cwd=root, check=False)
    if count.returncode != 0 or not count.stdout.strip().isdigit():
        raise GitToolsError("Cannot read commit history.")
    if int(count.stdout.strip()) < 1:
        raise GitToolsError("No commits to undo.")

    parents = _run_git(["rev-list", "--parents", "-n", "1", "HEAD"], cwd=root, check=False)
    if parents.returncode != 0:
        raise GitToolsError("Cannot read HEAD.")
    parent_parts = parents.stdout.strip().split()
    if len(parent_parts) < 2:
        raise GitToolsError("Cannot undo the initial commit.")

    if not confirm("Undo last commit (soft reset)? [y/N] ", stdin=stdin):
        return "Cancelled."

    _run_git(["reset", "--soft", "HEAD~1"], cwd=root)
    return "Undid last commit (changes kept staged)."


def _hook_path(root):
    return root / ".git" / "hooks" / HOOK_NAME


def hooks_install(cwd=None):
    root = git_root(cwd)
    hook_path = _hook_path(root)
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "#!/bin/sh\n"
        "{0}\n"
        "# Installed by Drico git hooks install\n"
        "exit 0\n"
    ).format(HOOK_MARKER)
    if hook_path.is_file():
        existing = hook_path.read_text(encoding="utf-8")
        if HOOK_MARKER in existing:
            return "Hook already installed at {0}.".format(hook_path)
        raise GitToolsError("Refusing to overwrite existing hook at {0}.".format(hook_path))
    hook_path.write_text(content, encoding="utf-8")
    os.chmod(hook_path, 0o755)
    return "Installed {0}.".format(hook_path)


def hooks_remove(cwd=None):
    root = git_root(cwd)
    hook_path = _hook_path(root)
    if not hook_path.is_file():
        return "No hook at {0}.".format(hook_path)
    text = hook_path.read_text(encoding="utf-8")
    if HOOK_MARKER not in text:
        raise GitToolsError("Hook at {0} was not installed by Drico.".format(hook_path))
    hook_path.unlink()
    return "Removed {0}.".format(hook_path)


def _args_after_command(context, command_words):
    raw_parts = context.raw.split()
    if len(raw_parts) <= len(command_words):
        return None
    norm_parts = context.normalized.split()
    if norm_parts[: len(command_words)] != command_words:
        return None
    return " ".join(raw_parts[len(command_words) :])


def _run_report(context, fn, command_words, path_kw=None):
    try:
        extra = _args_after_command(context, command_words)
        kwargs = {"cwd": Path.cwd()}
        if path_kw:
            kwargs[path_kw] = extra
        elif extra:
            if fn is git_summary:
                kwargs["commit_count"] = extra
            elif fn is hotspots_report:
                kwargs["limit"] = extra
            elif fn is stale_branches_report:
                kwargs["days"] = extra
        print(fn(**kwargs))
        print()
    except GitToolsError as exc:
        print("Drico > {0}\n".format(exc))


def _handle_undo_last(context):
    try:
        message = undo_last_commit(cwd=Path.cwd())
        if message:
            print("Drico > {0}\n".format(message))
    except GitToolsError as exc:
        print("Drico > {0}\n".format(exc))


def _handle_hooks(context):
    action = context.normalized.split()
    if len(action) < 2:
        print("Drico > Usage: hooks install | hooks remove\n")
        return
    verb = action[1]
    try:
        if verb == "install":
            print("Drico > {0}\n".format(hooks_install(cwd=Path.cwd())))
        elif verb == "remove":
            print("Drico > {0}\n".format(hooks_remove(cwd=Path.cwd())))
        else:
            print("Drico > Usage: hooks install | hooks remove\n")
    except GitToolsError as exc:
        print("Drico > {0}\n".format(exc))


def register(registry):
    category = "git"
    commands = [
        (
            "git summary",
            lambda c: _run_report(c, git_summary, ["git", "summary"]),
            "Repository summary.",
        ),
        (
            "hotspots",
            lambda c: _run_report(c, hotspots_report, ["hotspots"]),
            "Files touched most in history.",
        ),
        (
            "blame-summary",
            lambda c: _run_report(
                c, blame_summary, ["blame-summary"], path_kw="path"
            ),
            "Line counts by author for a file.",
        ),
        (
            "stale-branches",
            lambda c: _run_report(c, stale_branches_report, ["stale-branches"]),
            "Branches older than N days (default 30).",
        ),
        ("undo-last", _handle_undo_last, "Soft-reset the last commit.", True),
        ("hooks install", _handle_hooks, "Install Drico pre-commit hook."),
        ("hooks remove", _handle_hooks, "Remove Drico pre-commit hook.", True),
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
