"""Project folder packs: registry and pack naming."""

import hashlib
import json
from pathlib import Path

from drico_bot.knowledge.pack import get_drico_home, pack_dir

PROJECT_INDEX_FILENAME = "project_index.json"
PROJECT_PACK_PREFIX = "project-"


def project_index_path():
    return get_drico_home() / PROJECT_INDEX_FILENAME


def _load_project_index():
    path = project_index_path()
    if not path.is_file():
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        return {}
    return data


def _save_project_index(data):
    path = project_index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def pack_name_for_root(root_path):
    root = Path(root_path).resolve()
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    return PROJECT_PACK_PREFIX + digest


def register_project_root(root_path, pack_name):
    root = str(Path(root_path).resolve())
    data = _load_project_index()
    data[root] = {"pack_name": pack_name, "root": root}
    _save_project_index(data)


def _best_project_entry_for_cwd(cwd=None):
    """Return (root Path, pack_name) for the longest registered root containing cwd."""
    if cwd is None:
        cwd = Path.cwd()
    cwd = Path(cwd).resolve()
    data = _load_project_index()
    best_root = None
    best_pack = None
    for root_str, entry in data.items():
        if not isinstance(entry, dict):
            continue
        pack_name = entry.get("pack_name")
        if not pack_name:
            continue
        root = Path(root_str).resolve()
        try:
            cwd.relative_to(root)
        except ValueError:
            continue
        if best_root is None or len(str(root)) > len(str(best_root)):
            best_root = root
            best_pack = pack_name
    if best_root is None:
        return None, None
    if not pack_dir(best_pack).is_dir():
        return None, None
    return best_root, best_pack


def find_project_root_for_cwd(cwd=None):
    """Return project root Path for cwd, or None if not inside an indexed project."""
    root, _pack = _best_project_entry_for_cwd(cwd)
    return root


def find_project_pack_for_cwd(cwd=None):
    """
    Return pack name for the longest registered project root containing cwd.
    """
    _root, pack = _best_project_entry_for_cwd(cwd)
    return pack
