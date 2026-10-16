from drico_bot.knowledge.tokenize import STOPWORDS, tokenize


def test_tokenize_lowercases_and_splits_on_non_letters():
    tokens = tokenize("Hello, WORLD! Python3.11 rocks.")
    assert "hello" in tokens
    assert "world" in tokens
    assert "python" in tokens
    assert "rocks" in tokens
    assert "11" not in tokens


def test_tokenize_removes_stopwords():
    tokens = tokenize("the quick brown fox is in the forest")
    assert "the" not in tokens
    assert "is" not in tokens
    assert "in" not in tokens
    assert "quick" in tokens
    assert "brown" in tokens
    assert "fox" in tokens
    assert "forest" in tokens


def test_stopword_list_is_small_english_set():
    assert "and" in STOPWORDS
    assert "python" not in STOPWORDS
