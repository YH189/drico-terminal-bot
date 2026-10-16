import json
import os
from pathlib import Path

import pytest

from drico_bot.knowledge.folder_index import FolderIndexError, index_folder
from drico_bot.knowledge.pack import get_drico_home
from drico_bot.knowledge.project import find_project_pack_for_cwd
from drico_bot.knowledge.query import ask, search
from drico_bot.knowledge.synonyms import SynonymsError, load_synonyms
from drico_bot.knowledge.watch_folder import watch_folder
from drico_bot.plugins.knowledge import run_cli


def _write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_index_skips_rules_and_indexes_text(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "keep.md", "visible project knowledge token")
    _write(root / ".hidden.md", "hidden secret")
    _write(root / "node_modules" / "pkg.md", "dependency noise")
    _write(root / ".git" / "HEAD", "ref: refs/heads/main")
    _write(root / "big.md", "x" * (1024 * 1024 + 1))
    (root / "binary.bin").write_bytes(b"\x00\x01\x02\x03")

    pack_name, doc_count, file_count = index_folder(root)
    assert file_count == 1
    assert doc_count == 1
    assert pack_name.startswith("project-")

    hits = search("visible project knowledge", cwd=root)
    assert hits
    assert hits[0]["pack"] == pack_name


def test_index_symlink_escape(tmp_path, drico_home):
    outside = tmp_path / "outside"
    root = tmp_path / "proj"
    _write(outside / "leak.md", "outside leak secret token")
    _write(root / "safe.md", "inside safe token")
    root.mkdir(parents=True, exist_ok=True)
    (root / "escape-link.md").symlink_to(outside / "leak.md")

    pack_name, _doc_count, file_count = index_folder(root)
    assert file_count == 1

    assert search("outside leak", cwd=root) == []
    assert search("inside safe", cwd=root)


def test_synonyms_validated_on_load(drico_home):
    path = get_drico_home() / "synonyms.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"zebra": ["uniquezebraword"]}', encoding="utf-8")
    assert load_synonyms() == {"zebra": ["uniquezebraword"]}

    path.write_text('{"bad": 1}', encoding="utf-8")
    with pytest.raises(SynonymsError):
        load_synonyms()


def test_ask_expands_synonyms(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "doc.md", "The uniquezebraword appears here.")
    synonyms = get_drico_home() / "synonyms.json"
    synonyms.write_text(json.dumps({"zebra": ["uniquezebraword"]}), encoding="utf-8")
    index_folder(root)

    answer = ask("zebra", cwd=root)
    assert "uniquezebraword" in answer


def test_phrase_matching_quoted(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(
        root / "doc.md",
        "alpha beta gamma\nseparate alpha and beta lines\n",
    )
    index_folder(root)

    assert search('"alpha beta" gamma', cwd=root)
    assert search('"alpha beta" delta', cwd=root) == []


def test_ask_prefers_project_pack(tmp_path, drico_home):
    from drico_bot.knowledge.importer import import_path
    from drico_bot.knowledge.index import reindex_all

    project = tmp_path / "mine"
    _write(project / "local.md", "sharedterm projectonlymarker detail")
    index_folder(project)

    other = tmp_path / "other_fixture"
    _write(other / "global.md", "sharedterm globalonlymarker detail")
    import_path(str(other), "global-pack", license_value="CC0-1.0")
    reindex_all()

    hits = search("sharedterm detail", cwd=project)
    assert hits
    assert hits[0]["pack"].startswith("project-")
    assert "projectonlymarker" in hits[0]["text"]


def test_watch_reindexes_on_change(tmp_path, drico_home):
    root = tmp_path / "proj"
    _write(root / "doc.md", "watchtoken version one")
    index_folder(root)

    ticks = {"n": 0}

    def fake_sleep(_seconds):
        ticks["n"] += 1
        if ticks["n"] == 1:
            _write(root / "doc.md", "watchtoken version two updated")

    def should_continue():
        return ticks["n"] < 2

    watch_folder(root, poll_seconds=0.01, sleep_fn=fake_sleep, should_continue=should_continue)

    answer = ask("version two", cwd=root)
    assert "version two" in answer


def test_cli_index_and_ask_still_work(tmp_path, drico_home, capsys):
    root = tmp_path / "proj"
    _write(root / "cli.md", "clitest marker phrase")
    code = run_cli(["index", str(root)])
    assert code == 0
    out = capsys.readouterr().out
    assert "Indexed" in out

    code = run_cli(["ask", "clitest marker"])
    assert code == 0
    assert "clitest" in capsys.readouterr().out


def test_find_project_pack_nested_cwd(tmp_path, drico_home):
    root = tmp_path / "proj"
    sub = root / "src" / "deep"
    _write(sub / "doc.md", "nested marker")
    pack_name, _, _ = index_folder(root)
    assert find_project_pack_for_cwd(sub) == pack_name
