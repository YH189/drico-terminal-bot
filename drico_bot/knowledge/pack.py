"""Knowledge pack layout, manifest I/O, and integrity hashes."""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_FILENAME = "manifest.json"
SUPPORTED_SUFFIXES = (".txt", ".md", ".jsonl")
MAX_FILE_BYTES = 5 * 1024 * 1024


def get_drico_home():
    override = os.environ.get("DRICO_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".drico"


def get_packs_root():
    return get_drico_home() / "packs"


def get_knowledge_db_path():
    return get_drico_home() / "knowledge.db"


def pack_dir(pack_name):
    return get_packs_root() / pack_name


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def manifest_files_hash(manifest):
    """Stable hash of pack file contents (used to detect import changes)."""
    files = manifest.get("files") or {}
    canonical = json.dumps(files, sort_keys=True, separators=(",", ":"))
    return sha256_bytes(canonical.encode("utf-8"))


def load_manifest(path):
    manifest_path = path / MANIFEST_FILENAME if path.is_dir() else path
    with open(manifest_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_manifest(pack_path, manifest):
    pack_path = Path(pack_path)
    pack_path.mkdir(parents=True, exist_ok=True)
    manifest_path = pack_path / MANIFEST_FILENAME
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")


def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def list_installed_packs():
    root = get_packs_root()
    if not root.is_dir():
        return []
    names = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / MANIFEST_FILENAME).is_file():
            names.append(child.name)
    return names


def pack_size_bytes(pack_path):
    total = 0
    for dirpath, _dirnames, filenames in os.walk(pack_path):
        for name in filenames:
            total += (Path(dirpath) / name).stat().st_size
    return total


def is_probably_text_file(path):
    try:
        with open(path, "rb") as handle:
            sample = handle.read(8192)
    except OSError:
        return False
    if not sample:
        return True
    if b"\x00" in sample:
        return False
    try:
        sample.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def relative_pack_path(pack_path, file_path):
    return str(file_path.relative_to(pack_path)).replace("\\", "/")


def build_files_hash_map(pack_path):
    """Map relative paths to sha256 for all non-manifest files under the pack."""
    files = {}
    for dirpath, _dirnames, filenames in os.walk(pack_path):
        for name in filenames:
            if name == MANIFEST_FILENAME:
                continue
            full = Path(dirpath) / name
            rel = relative_pack_path(pack_path, full)
            files[rel] = sha256_file(full)
    return files


def verify_pack(pack_path):
    """Return list of (relative_path, expected, actual) for mismatches."""
    pack_path = Path(pack_path)
    manifest = load_manifest(pack_path)
    expected = manifest.get("files") or {}
    mismatches = []
    for rel, want in sorted(expected.items()):
        target = pack_path / rel
        if not target.is_file():
            mismatches.append((rel, want, None))
            continue
        got = sha256_file(target)
        if got != want:
            mismatches.append((rel, want, got))
    return mismatches
