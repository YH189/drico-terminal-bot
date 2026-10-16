"""Index a local folder into a project knowledge pack (offline, stdlib-only)."""

import json
import os
import shutil
from pathlib import Path

from drico_bot.knowledge.importer import _count_text_docs
from drico_bot.knowledge.index import _connect, _rebuild_global_stats, index_pack, init_db
from drico_bot.knowledge.pack import (
    MANIFEST_FILENAME,
    SUPPORTED_SUFFIXES,
    build_files_hash_map,
    get_drico_home,
    get_packs_root,
    is_probably_text_file,
    pack_dir,
    utc_now_iso,
    write_manifest,
)
from drico_bot.knowledge.project import pack_name_for_root, register_project_root

INDEX_SKIP_DIR_NAMES = frozenset(
    {".git", "node_modules", "__pycache__", "venv"}
)
MAX_INDEX_FILE_BYTES = 1024 * 1024


class FolderIndexError(Exception):
    """User-facing folder index failure."""


def _path_stays_under_root(root, candidate):
    root = Path(root).resolve()
    try:
        candidate = candidate.resolve()
    except OSError:
        return False
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _should_skip_dir(name):
    if name.startswith("."):
        return True
    return name in INDEX_SKIP_DIR_NAMES


def _should_skip_file(name):
    return name.startswith(".")


def _iter_index_files(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise FolderIndexError("Not a directory: {0}".format(root))

    for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current = Path(dirpath)
        if not _path_stays_under_root(root, current):
            dirnames[:] = []
            continue

        pruned = []
        for name in dirnames:
            if _should_skip_dir(name):
                continue
            child = current / name
            if child.is_symlink():
                if not _path_stays_under_root(root, child):
                    continue
            pruned.append(name)
        dirnames[:] = pruned

        for name in filenames:
            if name == MANIFEST_FILENAME:
                continue
            if _should_skip_file(name):
                continue
            src = current / name
            if src.is_symlink():
                if not _path_stays_under_root(root, src):
                    continue
            if not _path_stays_under_root(root, src):
                continue
            suffix = src.suffix.lower()
            if suffix not in SUPPORTED_SUFFIXES:
                continue
            try:
                size = src.stat().st_size
            except OSError:
                continue
            if size > MAX_INDEX_FILE_BYTES:
                continue
            if not is_probably_text_file(src):
                continue
            rel = str(src.relative_to(root)).replace("\\", "/")
            yield rel, src


def _wipe_pack_contents(pack_path):
    pack_path = Path(pack_path)
    if not pack_path.is_dir():
        pack_path.mkdir(parents=True, exist_ok=True)
        return
    for child in pack_path.iterdir():
        if child.name == MANIFEST_FILENAME:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def index_folder(folder_path, license_value="CC0-1.0", source_url=""):
    """
    Sync supported text files from folder into ~/.drico/packs/<project-pack>/.
    Returns (pack_name, doc_count, file_count).
    """
    root = Path(folder_path)
    if not root.exists():
        raise FolderIndexError("Folder does not exist: {0}".format(folder_path))
    root = root.resolve()
    if not root.is_dir():
        raise FolderIndexError("Not a directory: {0}".format(folder_path))

    pack_name = pack_name_for_root(root)
    destination = pack_dir(pack_name)
    get_drico_home().mkdir(parents=True, exist_ok=True)
    get_packs_root().mkdir(parents=True, exist_ok=True)

    _wipe_pack_contents(destination)

    file_count = 0
    for rel, src in _iter_index_files(root):
        dest = destination / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        file_count += 1

    if file_count == 0:
        raise FolderIndexError(
            "No indexable documents found (.txt, .md, .jsonl under 1 MB)."
        )

    doc_count = _count_text_docs(destination)
    files = build_files_hash_map(destination)
    existing_license = license_value
    existing_version = "1.0.0"
    existing_source = source_url or "file://{0}".format(root)
    manifest_path = destination / MANIFEST_FILENAME
    if manifest_path.is_file():
        with open(manifest_path, "r", encoding="utf-8") as handle:
            old = json.load(handle)
        existing_license = old.get("license") or existing_license
        existing_version = old.get("version") or existing_version
        if not source_url:
            existing_source = old.get("source_url") or existing_source

    manifest = {
        "name": pack_name,
        "version": existing_version,
        "source_url": existing_source,
        "license": existing_license,
        "created_at": utc_now_iso(),
        "doc_count": doc_count,
        "chunk_count": 0,
        "files": files,
        "project_root": str(root),
    }
    write_manifest(destination, manifest)
    register_project_root(root, pack_name)

    conn = _connect()
    init_db(conn)
    index_pack(conn, pack_name, force=True)
    _rebuild_global_stats(conn)
    conn.commit()
    conn.close()

    return pack_name, doc_count, file_count


def index_folder_text(folder_path):
    try:
        pack_name, doc_count, file_count = index_folder(folder_path)
    except FolderIndexError as exc:
        return str(exc)
    return "Indexed {0} file(s) ({1} documents) into pack '{2}'.".format(
        file_count, doc_count, pack_name
    )
