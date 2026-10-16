from pathlib import Path

from drico_bot.knowledge.importer import import_path
from drico_bot.knowledge.index import (
    _connect,
    get_stored_manifest_hash,
    init_db,
    manifest_files_hash,
    reindex_all,
)
from drico_bot.knowledge.pack import load_manifest, pack_dir

FIXTURE = Path(__file__).parent / "fixtures" / "python_docs_pack"


def test_reindex_skips_unchanged_manifest(drico_home):
    import_path(str(FIXTURE), "incr-pack", license_value="CC0-1.0")
    first = reindex_all()
    assert "incr-pack" in first

    second = reindex_all()
    assert second == []

    manifest = load_manifest(pack_dir("incr-pack"))
    conn = _connect()
    init_db(conn)
    stored = get_stored_manifest_hash(conn, "incr-pack")
    conn.close()
    assert stored == manifest_files_hash(manifest)
