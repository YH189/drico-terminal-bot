"""Load and validate ~/.drico/synonyms.json for query expansion."""

import json
from pathlib import Path

from drico_bot.knowledge.pack import get_drico_home

SYNONYMS_FILENAME = "synonyms.json"


class SynonymsError(ValueError):
    """Invalid synonyms configuration."""


def synonyms_path():
    return get_drico_home() / SYNONYMS_FILENAME


def _validate_synonyms_data(data):
    if not isinstance(data, dict):
        raise SynonymsError("synonyms.json must be a JSON object.")
    validated = {}
    for key, value in data.items():
        if not isinstance(key, str) or not key.strip():
            raise SynonymsError("synonyms.json keys must be non-empty strings.")
        if not isinstance(value, list):
            raise SynonymsError(
                "synonyms.json value for '{0}' must be a list.".format(key)
            )
        phrases = []
        for item in value:
            if not isinstance(item, str):
                raise SynonymsError(
                    "synonyms.json entries for '{0}' must be strings.".format(key)
                )
            text = item.strip()
            if text:
                phrases.append(text)
        validated[key.strip().lower()] = phrases
    return validated


def load_synonyms():
    """
    Return mapping canonical_term -> list of synonym phrases.
    Missing file returns {}. Invalid file raises SynonymsError.
    """
    path = synonyms_path()
    if not path.is_file():
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return _validate_synonyms_data(data)


def expand_query_tokens(tokens, synonyms):
    """Add tokens from synonym phrases for any token that matches a key."""
    if not synonyms or not tokens:
        return list(tokens)
    expanded = []
    seen = set()
    for token in tokens:
        if token not in seen:
            expanded.append(token)
            seen.add(token)
        for phrase in synonyms.get(token, ()):
            for part in phrase.lower().split():
                if part and part not in seen:
                    expanded.append(part)
                    seen.add(part)
    return expanded
