"""Download knowledge packs from curated sources.json (Phase 11 — only network module)."""

import io
import json
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from drico_bot.knowledge.importer import PackImportError
from drico_bot.knowledge.pack import (
    MANIFEST_FILENAME,
    build_files_hash_map,
    get_packs_root,
    pack_dir,
    utc_now_iso,
    write_manifest,
)

ALLOWED_LICENSES = frozenset(
    {
        "CC0-1.0",
        "CC-BY-4.0",
        "CC-BY-SA-4.0",
        "MIT",
        "Apache-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "PSF-2.0",
        "Public-Domain",
    }
)

MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024
SOURCES_PATH = Path(__file__).resolve().parent.parent / "data" / "sources.json"


class PackDownloadError(Exception):
    """User-facing pack download failure."""


def _load_catalog(path=None):
    path = Path(path) if path else SOURCES_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PackDownloadError("Cannot read sources catalog: {0}".format(path)) from exc
    sources = data.get("sources") or []
    if not isinstance(sources, list):
        raise PackDownloadError("Invalid sources catalog format.")
    return sources


def _find_source(sources, name):
    for entry in sources:
        if isinstance(entry, dict) and entry.get("name") == name:
            return entry
    return None


def _fetch_url(url, max_bytes):
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            chunks = []
            total = 0
            while True:
                block = response.read(65536)
                if not block:
                    break
                total += len(block)
                if total > max_bytes:
                    raise PackDownloadError(
                        "Download exceeds size cap ({0} bytes).".format(max_bytes)
                    )
                chunks.append(block)
    except urllib.error.URLError as exc:
        raise PackDownloadError("Download failed: {0}".format(exc)) from exc
    return b"".join(chunks)


def _safe_extract_zip(data, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            target = (destination / info.filename).resolve()
            if not str(target).startswith(str(destination.resolve())):
                raise PackDownloadError("Unsafe path in pack archive.")
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as src, open(target, "wb") as dest:
                dest.write(src.read())


def _count_docs(pack_path):
    from drico_bot.knowledge.importer import _count_text_docs

    return _count_text_docs(pack_path)


def download_pack(name, sources_path=None):
    """Download pack `name` from bundled sources.json and install under ~/.drico/packs/."""
    sources = _load_catalog(sources_path)
    entry = _find_source(sources, name)
    if entry is None:
        raise PackDownloadError("Unknown pack source: {0}".format(name))

    url = str(entry.get("url") or "").strip()
    if not url:
        raise PackDownloadError("Source entry has no url.")

    license_value = str(entry.get("license") or "").strip()
    if license_value not in ALLOWED_LICENSES:
        raise PackDownloadError("License not allowed: {0}".format(license_value))

    expected_sha = str(entry.get("sha256") or "").strip().lower()
    if not expected_sha:
        raise PackDownloadError("Source entry missing sha256.")

    max_bytes = int(entry.get("max_bytes") or MAX_DOWNLOAD_BYTES)
    if max_bytes <= 0 or max_bytes > MAX_DOWNLOAD_BYTES:
        max_bytes = MAX_DOWNLOAD_BYTES

    allowed_urls = {str(item.get("url") or "").strip() for item in sources if isinstance(item, dict)}
    if url not in allowed_urls:
        raise PackDownloadError("URL is not listed in sources catalog.")

    destination = pack_dir(name)
    if destination.exists():
        raise PackDownloadError("Pack already installed: {0}".format(name))

    get_packs_root().mkdir(parents=True, exist_ok=True)
    payload = _fetch_url(url, max_bytes)

    import hashlib

    digest = hashlib.sha256(payload).hexdigest()
    if digest != expected_sha:
        raise PackDownloadError("SHA-256 mismatch for downloaded pack.")

    staging = destination.with_suffix(".staging")
    if staging.exists():
        import shutil

        shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True, exist_ok=True)

    if payload[:2] == b"PK":
        _safe_extract_zip(payload, staging)
    else:
        raise PackDownloadError("Pack download must be a zip archive.")

    doc_count = _count_docs(staging)
    if doc_count == 0:
        import shutil

        shutil.rmtree(staging, ignore_errors=True)
        raise PackDownloadError("Downloaded pack has no supported documents.")

    files = build_files_hash_map(staging)
    manifest = {
        "name": name,
        "version": str(entry.get("version") or "1.0.0"),
        "source_url": url,
        "license": license_value,
        "created_at": utc_now_iso(),
        "doc_count": doc_count,
        "chunk_count": 0,
        "files": files,
    }
    write_manifest(staging, manifest)
    staging.rename(destination)
    return "Downloaded pack '{0}' ({1} documents). Run 'reindex'.".format(name, doc_count)
