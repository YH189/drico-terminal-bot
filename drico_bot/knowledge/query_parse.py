"""Parse ask/search queries for quoted phrases and free text."""

import re

_PHRASE_RE = re.compile(r'"([^"]+)"')


def parse_question(question):
    """
    Return (phrases, remainder_text).
    phrases are lowercased strings without surrounding quotes.
    """
    phrases = []
    for match in _PHRASE_RE.finditer(question):
        text = match.group(1).strip()
        if text:
            phrases.append(text.lower())
    remainder = _PHRASE_RE.sub(" ", question)
    return phrases, remainder.strip()


def chunk_contains_phrases(text, phrases):
    if not phrases:
        return True
    lowered = text.lower()
    for phrase in phrases:
        if phrase not in lowered:
            return False
    return True
