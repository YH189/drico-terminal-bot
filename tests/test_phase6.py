import os
from pathlib import Path

import pytest

from drico_bot.core.dispatcher import Dispatcher, InteractiveSession
from drico_bot.core.registry import Registry
from drico_bot.knowledge.folder_index import index_folder
from drico_bot.plugins.code_intel import (
    CodeIntelError,
    complexity_report,
    deps_report,
    explain_file,
    largefiles_report,
    loc_report,
    resolve_code_path,
    scan_secrets,
    todos_report,
)
from drico_bot.plugins.code_intel import register as register_code_intel


def _write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _index_project(root):
    """Register project root via index (needs at least one .md/.txt/.jsonl file)."""
    readme = Path(root) / "README.md"
    if not readme.is_file():
        _write(readme, "project\n")
    index_folder(root)


def _registry():
    reg = Registry()
    register_code_intel(reg)
    return reg


def _dispatch(raw, registry, cwd):
    session = InteractiveSession()
    session.registry = registry
    dispatcher = Dispatcher(registry)
    old = os.getcwd()
    os.chdir(cwd)
    try:
        normalized = raw.lower().strip()
        dispatcher.dispatch(raw, normalized, session)
    finally:
        os.chdir(old)


def test_resolve_rejects_unindexed(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "a.py", "x = 1\n")
    with pytest.raises(CodeIntelError, match="indexed project"):
        resolve_code_path("a.py", cwd=root)


def test_resolve_blocks_symlink_escape(tmp_path, drico_home):
    outside = tmp_path / "outside"
    root = tmp_path / "proj"
    _write(outside / "leak.py", "x = 1\n")
    _write(root / "ok.py", "y = 2\n")
    root.mkdir(parents=True, exist_ok=True)
    (root / "link.py").symlink_to(outside / "leak.py")
    _index_project(root)
    with pytest.raises(CodeIntelError, match="escapes"):
        resolve_code_path("link.py", cwd=root)


def test_explain_file_python(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(
        root / "mod.py",
        '"""Module doc."""\nimport os\n\nclass Foo:\n    def bar(self):\n        pass\n\ndef baz():\n    return 1\n',
    )
    _index_project(root)
    text = explain_file(path="mod.py", cwd=root)
    assert "mod.py" in text
    assert "Module doc" in text
    assert "Foo" in text
    assert "baz" in text


def test_complexity_orders_functions(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(
        root / "hard.py",
        "def easy():\n    return 1\n\n"
        "def hard():\n"
        "    if 1:\n        if 2:\n            for x in range(3):\n                pass\n"
        "    return 0\n",
    )
    _index_project(root)
    text = complexity_report(path="hard.py", cwd=root)
    assert "hard" in text
    assert "easy" in text
    hard_line = [line for line in text.splitlines() if "hard.py:hard" in line][0]
    easy_line = [line for line in text.splitlines() if "hard.py:easy" in line][0]
    assert int(hard_line.strip().split()[0]) > int(easy_line.strip().split()[0])


def test_secrets_masked(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "config.py", 'API_KEY = "abcdefghijklmnop"\n')
    _index_project(root)
    text = scan_secrets(path="config.py", cwd=root)
    assert "abcd***" in text
    assert "abcdefghijklmnop" not in text


def test_deps_from_requirements(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "requirements.txt", "requests>=2.0\n# comment\npytest\n")
    _index_project(root)
    text = deps_report(path=None, cwd=root)
    assert "requests" in text
    assert "pytest" in text


def test_todos_found(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "work.py", "# TODO: ship feature\npass\n")
    _index_project(root)
    text = todos_report(path=None, cwd=root)
    assert "TODO" in text
    assert "ship feature" in text


def test_loc_counts(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "a.py", "line1\nline2\n")
    _write(root / "b.md", "only\n")
    _index_project(root)
    text = loc_report(path=None, cwd=root)
    assert ".py: 2" in text
    assert ".md" in text


def test_largefiles(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "small.txt", "x\n")
    big = root / "big.bin"
    big.write_bytes(b"x" * (100 * 1024))
    _index_project(root)
    text = largefiles_report(path=None, cwd=root, min_bytes=100 * 1024)
    assert "big.bin" in text
    assert "small.txt" not in text


def test_dispatch_explain_file(tmp_path, drico_home, capsys):
    root = tmp_path / "proj"
    _write(root / "x.py", "def fn():\n    pass\n")
    _index_project(root)
    reg = _registry()
    _dispatch("explain-file x.py", reg, root)
    out = capsys.readouterr().out
    assert "x.py" in out
    assert "fn" in out
