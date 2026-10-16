from pathlib import Path

from drico_bot.knowledge.importer import import_path
from drico_bot.knowledge.index import reindex_all
from drico_bot.knowledge.query import search


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "bm25_corpus"


def _write_corpus():
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    docs = {
        "alpha.txt": "Alpha document about rivers and rainfall patterns.",
        "beta.txt": "Beta document about database indexes and btree structures.",
        "gamma.txt": "Gamma document about gamma rays and particle physics.",
        "delta.txt": "Delta document about river deltas and sediment transport.",
        "epsilon.txt": "Epsilon document about small constants in mathematics.",
    }
    for name, body in docs.items():
        path = FIXTURE_DIR / name
        if not path.exists():
            path.write_text(body, encoding="utf-8")


def test_bm25_prefers_river_delta_document(drico_home):
    _write_corpus()
    import_path(
        str(FIXTURE_DIR),
        "bm25-fixture",
        license_value="CC0-1.0",
        source_url="fixture://bm25",
    )
    reindex_all()
    hits = search("river delta sediment", top_k=3)
    assert hits
    assert hits[0]["title"] == "delta.txt"
    assert hits[0]["pack"] == "bm25-fixture"
