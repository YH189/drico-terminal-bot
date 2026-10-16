from pathlib import Path

import pytest

from drico_bot.knowledge.importer import PackImportError, import_path
from drico_bot.knowledge.manager import verify_all_packs_text
from drico_bot.knowledge.pack import pack_dir, verify_pack

FIXTURE = Path(__file__).parent / "fixtures" / "python_docs_pack"


def test_import_rejects_missing_license(drico_home):
    with pytest.raises(PackImportError) as exc:
        import_path(str(FIXTURE), "no-license-pack", license_value=None)
    assert "License is required" in str(exc.value)


def test_import_creates_manifest_with_hashes(drico_home):
    manifest = import_path(
        str(FIXTURE),
        "python-docs",
        license_value="CC0-1.0",
        source_url="fixture://python_docs_pack",
    )
    assert manifest["license"] == "CC0-1.0"
    assert manifest["doc_count"] == 5
    assert len(manifest["files"]) == 3
    assert (pack_dir("python-docs") / "manifest.json").is_file()


def test_verify_detects_modified_file(drico_home):
    import_path(str(FIXTURE), "verify-pack", license_value="MIT")
    target = pack_dir("verify-pack") / "list_comprehension.txt"
    with open(target, "a", encoding="utf-8") as handle:
        handle.write("\n# tampered\n")
    mismatches = verify_pack(pack_dir("verify-pack"))
    assert len(mismatches) == 1
    report = verify_all_packs_text()
    assert "CORRUPT" in report
