"""Import local folders or files into a knowledge pack."""

import os
import shutil
from pathlib import Path

from drico_bot.knowledge.pack import (
    MANIFEST_FILENAME,
    MAX_FILE_BYTES,
    SUPPORTED_SUFFIXES,
    build_files_hash_map,
    get_packs_root,
    is_probably_text_file,
    pack_dir,
    utc_now_iso,
    write_manifest,
)


class PackImportError(Exception):
    """User-facing import failure."""


def _ensure_license(license_value):
    if license_value is None or not str(license_value).strip():
        raise PackImportError(
            "License is required. Add one with --license (for example CC0-1.0 or MIT)."
        )
    return str(license_value).strip()


def _copy_tree_filtered(source, destination):
    source = Path(source)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for dirpath, _dirnames, filenames in os.walk(source):
        rel_dir = Path(dirpath).relative_to(source)
        for name in filenames:
            src = Path(dirpath) / name
            if src.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue
            if src.stat().st_size > MAX_FILE_BYTES:
                continue
            if not is_probably_text_file(src):
                continue
            dest = destination / rel_dir / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


def _import_single_file(source, destination_pack):
    source = Path(source)
    if source.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise PackImportError(
            "Unsupported file type. Supported extensions: .txt, .md, .jsonl"
        )
    if source.stat().st_size > MAX_FILE_BYTES:
        raise PackImportError("File exceeds the 5 MB import limit.")
    if not is_probably_text_file(source):
        raise PackImportError("Binary files cannot be imported.")
    destination_pack.mkdir(parents=True, exist_ok=True)
    dest = destination_pack / source.name
    shutil.copy2(source, dest)


def _count_text_docs(pack_path):
    count = 0
    for dirpath, _dirnames, filenames in os.walk(pack_path):
        for name in filenames:
            if name == MANIFEST_FILENAME:
                continue
            suffix = Path(name).suffix.lower()
            if suffix in (".txt", ".md"):
                count += 1
            elif suffix == ".jsonl":
                path = Path(dirpath) / name
                with open(path, "r", encoding="utf-8") as handle:
                    for line in handle:
                        if line.strip():
                            count += 1
    return count


def import_path(
    source_path,
    pack_name,
    license_value,
    version="1.0.0",
    source_url="",
):
    """
    Copy or read documents into ~/.drico/packs/<pack-name>/ and write manifest.json.
    """
    license_value = _ensure_license(license_value)
    source_path = Path(source_path)
    if not source_path.exists():
        raise PackImportError("Source path does not exist: {0}".format(source_path))

    destination = pack_dir(pack_name)
    if destination.exists():
        raise PackImportError(
            "Pack already exists: {0}. Choose a different --name.".format(pack_name)
        )

    get_packs_root().mkdir(parents=True, exist_ok=True)

    if source_path.is_dir():
        _copy_tree_filtered(source_path, destination)
    else:
        _import_single_file(source_path, destination)

    doc_count = _count_text_docs(destination)
    if doc_count == 0:
        shutil.rmtree(destination, ignore_errors=True)
        raise PackImportError(
            "No supported documents found (.txt, .md, .jsonl under 5 MB)."
        )

    files = build_files_hash_map(destination)
    manifest = {
        "name": pack_name,
        "version": version,
        "source_url": source_url or "",
        "license": license_value,
        "created_at": utc_now_iso(),
        "doc_count": doc_count,
        "chunk_count": 0,
        "files": files,
    }
    write_manifest(destination, manifest)
    return manifest
