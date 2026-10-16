from drico_bot.knowledge.query import NOT_FOUND_MESSAGE, ask, search


def test_not_found_when_index_empty(drico_home):
    assert search("quantum chromodynamics lattice") == []
    assert ask("quantum chromodynamics lattice") == NOT_FOUND_MESSAGE


def test_not_found_when_only_stopwords(drico_home):
    assert search("the and or") == []
    assert ask("the and or") == NOT_FOUND_MESSAGE
