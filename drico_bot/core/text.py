import re


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[?!.,;:]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text
