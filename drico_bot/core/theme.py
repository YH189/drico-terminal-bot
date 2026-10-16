"""ANSI themes with NO_COLOR and plain-mode support (Phase 10)."""

import os

from drico_bot.core.config import get, load_config

_STYLES = {
    "default": {
        "banner": ("\033[1m", "\033[0m"),
        "prompt": ("\033[36m", "\033[0m"),
        "accent": ("\033[33m", "\033[0m"),
        "error": ("\033[31m", "\033[0m"),
    },
    "plain": {},
}


def _theme_name(config=None):
    if config is None:
        config = load_config()
    name = get(config, "ui.theme", "default") or "default"
    if name not in _STYLES:
        return "default"
    return name


def colors_enabled(config=None):
    if os.environ.get("NO_COLOR"):
        return False
    return _theme_name(config) != "plain"


def style(text, kind="accent", config=None):
    if not colors_enabled(config):
        return text
    theme = _STYLES.get(_theme_name(config), _STYLES["default"])
    pair = theme.get(kind)
    if not pair:
        return text
    return "{0}{1}{2}".format(pair[0], text, pair[1])
