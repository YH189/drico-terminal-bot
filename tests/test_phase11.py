import hashlib
import io
import json
import zipfile
from pathlib import Path
from unittest import mock

import pytest

from drico_bot.knowledge.download import (
    PackDownloadError,
    download_pack,
)


def _build_zip_with_doc():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("readme.md", "# Hello pack\n")
    return buf.getvalue()


def test_download_pack_verifies_sha_and_installs(tmp_path, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    payload = _build_zip_with_doc()
    sha = hashlib.sha256(payload).hexdigest()
    catalog = {
        "sources": [
            {
                "name": "demo-pack",
                "url": "https://example.com/demo.zip",
                "license": "MIT",
                "sha256": sha,
                "version": "1.0.0",
            }
        ]
    }
    catalog_path = tmp_path / "sources.json"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

    with mock.patch(
        "drico_bot.knowledge.download._fetch_url", return_value=payload
    ):
        message = download_pack("demo-pack", sources_path=catalog_path)

    assert "Downloaded pack" in message
    pack_root = tmp_path / "packs" / "demo-pack"
    assert (pack_root / "manifest.json").is_file()
    assert (pack_root / "readme.md").is_file()


def test_download_rejects_bad_license(tmp_path, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    payload = _build_zip_with_doc()
    sha = hashlib.sha256(payload).hexdigest()
    catalog = {
        "sources": [
            {
                "name": "bad",
                "url": "https://example.com/b.zip",
                "license": "Proprietary",
                "sha256": sha,
            }
        ]
    }
    catalog_path = tmp_path / "sources.json"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    with mock.patch(
        "drico_bot.knowledge.download._fetch_url", return_value=payload
    ):
        with pytest.raises(PackDownloadError, match="License not allowed"):
            download_pack("bad", sources_path=catalog_path)


def test_network_only_in_download_module():
    import pathlib

    root = pathlib.Path("drico_bot")
    offenders = []
    for path in root.rglob("*.py"):
        if path.name == "download.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "urllib.request" in text or "urlopen" in text:
            offenders.append(str(path))
    assert offenders == []
