from pathlib import Path

from drico_bot.knowledge.importer import import_path
from drico_bot.knowledge.index import reindex_all
from drico_bot.knowledge.manager import list_packs_text
from drico_bot.knowledge.query import ask, search

FIXTURE = Path(__file__).parent / "fixtures" / "python_docs_pack"


def test_full_pipeline_import_reindex_ask(drico_home):
    import_path(
        str(FIXTURE),
        "python-docs",
        license_value="CC0-1.0",
        source_url="fixture://python_docs_pack",
    )
    changed = reindex_all()
    assert changed == ["python-docs"]

    listing = list_packs_text()
    assert "python-docs" in listing
    assert "CC0-1.0" in listing

    hits = search("trailing if condition evens filter", top_k=1)
    assert hits
    assert hits[0]["title"] == "list_comprehension.txt"

    answer = ask("dict get default KeyError")
    assert "dict-get" in answer or "dict.get" in answer
    assert "fixture://python_docs_pack/dict-get" in answer
