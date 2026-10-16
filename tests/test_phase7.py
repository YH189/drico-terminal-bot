import io
import os
import subprocess
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

from drico_bot.core.dispatcher import Dispatcher, InteractiveSession
from drico_bot.core.registry import Registry
from drico_bot.plugins.git_tools import (
    GitToolsError,
    blame_summary,
    git_root,
    git_summary,
    hooks_install,
    hooks_remove,
    hotspots_report,
    register,
    stale_branches_report,
    undo_last_commit,
)


def _run_git(args, cwd):
    subprocess.run(["git"] + list(args), cwd=str(cwd), check=True, capture_output=True)


def _init_repo(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    _run_git(["init"], path)
    _run_git(["config", "user.email", "test@example.com"], path)
    _run_git(["config", "user.name", "Test User"], path)


def _commit(path, message, filename="file.txt", content="line\n", env=None, date=None):
    file_path = Path(path) / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    _run_git(["add", filename], path)
    commit_env = os.environ.copy()
    if env:
        commit_env.update(env)
    if date:
        commit_env["GIT_AUTHOR_DATE"] = date
        commit_env["GIT_COMMITTER_DATE"] = date
    cmd = ["git", "commit", "-m", message]
    if date:
        cmd.extend(["--date", date])
    subprocess.run(
        cmd,
        cwd=str(path),
        check=True,
        capture_output=True,
        env=commit_env,
    )


def _registry():
    reg = Registry()
    register(reg)
    return reg


def _dispatch(raw, registry, cwd, confirm_yes=False, confirm_no=False):
    session = InteractiveSession()
    session.registry = registry
    dispatcher = Dispatcher(registry)
    old = os.getcwd()
    os.chdir(cwd)
    patches = []
    if confirm_yes:
        patches.append(
            mock.patch("drico_bot.plugins.git_tools.confirm", return_value=True)
        )
    if confirm_no:
        patches.append(
            mock.patch("drico_bot.plugins.git_tools.confirm", return_value=False)
        )
    for patcher in patches:
        patcher.start()
    try:
        dispatcher.dispatch(raw, raw.lower().strip(), session)
    finally:
        for patcher in reversed(patches):
            patcher.stop()
        os.chdir(old)


def test_git_root_requires_repo(tmp_path):
    with pytest.raises(GitToolsError, match="Not a git"):
        git_root(tmp_path)


def test_git_summary_lists_branch_and_commits(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "first", "a.txt", "a\n")
    _commit(repo, "second", "b.txt", "b\n")
    text = git_summary(cwd=repo, commit_count=2)
    assert "Branch: master" in text or "Branch: main" in text
    assert "second" in text
    assert "Changed files: 0" in text


def test_hotspots_orders_by_touches(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "one", "hot.txt", "1\n")
    _commit(repo, "two", "hot.txt", "2\n")
    _commit(repo, "three", "cold.txt", "x\n")
    text = hotspots_report(cwd=repo, limit=5)
    assert "hot.txt" in text
    hot_line = [line for line in text.splitlines() if "hot.txt" in line][0]
    cold_line = [line for line in text.splitlines() if "cold.txt" in line][0]
    assert int(hot_line.strip().split()[0]) > int(cold_line.strip().split()[0])


def test_blame_summary_counts_authors(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "alpha", "src.py", "one\n")
    text = blame_summary("src.py", cwd=repo)
    assert "Blame summary for src.py" in text
    assert "Test User" in text
    assert "Lines: 1" in text


def test_stale_branches_lists_old_branch(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    stale_tip_date = "2020-01-15T10:00:00"
    fresh_tip_date = "2025-05-01T10:00:00"
    report_now = datetime(2025, 6, 1, 12, 0, 0)

    _commit(repo, "old", "old.txt", "old\n", date=stale_tip_date)
    _run_git(["branch", "stale-branch"], repo)
    _commit(repo, "fresh", "fresh.txt", "new\n", date=fresh_tip_date)

    class _FixedNow(datetime):
        @classmethod
        def utcnow(cls):
            return report_now

    with mock.patch("drico_bot.plugins.git_tools.datetime", _FixedNow):
        text = stale_branches_report(cwd=repo, days=30)
    assert "stale-branch" in text


def test_undo_last_cancelled(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "first", "x.txt", "x\n")
    _commit(repo, "second", "y.txt", "y\n")
    message = undo_last_commit(cwd=repo, stdin=io.StringIO("n\n"))
    assert message == "Cancelled."
    log = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    assert log.stdout.strip() == "2"


def test_undo_last_confirmed_soft_reset(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "first", "a.txt", "a\n")
    _commit(repo, "second", "b.txt", "b\n")
    message = undo_last_commit(cwd=repo, stdin=io.StringIO("yes\n"))
    assert "Undid last commit" in message
    log = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    assert log.stdout.strip() == "1"
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    assert "b.txt" in status.stdout


def test_hooks_install_and_remove(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "init", "README.md", "hi\n")
    installed = hooks_install(cwd=repo)
    assert "Installed" in installed
    hook = repo / ".git" / "hooks" / "pre-commit"
    assert hook.is_file()
    assert hook.read_text(encoding="utf-8").find("drico-git-hooks") >= 0
    again = hooks_install(cwd=repo)
    assert "already installed" in again.lower()
    removed = hooks_remove(cwd=repo)
    assert "Removed" in removed
    assert not hook.is_file()


def test_hooks_remove_refuses_foreign_hook(tmp_path):
    repo = tmp_path / "repo"
    _init_repo(repo)
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    with pytest.raises(GitToolsError, match="not installed by Drico"):
        hooks_remove(cwd=repo)


def test_dispatch_git_summary(tmp_path, capsys):
    repo = tmp_path / "repo"
    _init_repo(repo)
    _commit(repo, "hello", "z.txt", "z\n")
    reg = _registry()
    _dispatch("git summary", reg, repo)
    out = capsys.readouterr().out
    assert "Git summary" in out
    assert "hello" in out